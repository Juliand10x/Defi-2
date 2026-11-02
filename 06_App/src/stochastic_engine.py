from dataclasses import dataclass
from typing import Dict, Optional, Tuple
import numpy as np
import pandas as pd
from scipy import stats, optimize


@dataclass
class SimulationResult:
    model_name: str
    ticker: str
    spot: float
    horizon_days: int
    n_paths: int
    time_grid: np.ndarray  # in days
    paths: np.ndarray       # shape (n_paths, horizon_days + 1)
    percentiles: Dict[int, np.ndarray]  # 10, 25, 50, 75, 90
    simulated_mean: float
    theoretical_mean: float
    std_error: float
    var_95: float  # In % and USD
    var_99: float
    cvar_95: float
    cvar_99: float
    parameters: Dict[str, float]
    log_likelihood: float
    aic: float
    bic: float


def calibrate_gbm(returns: pd.Series) -> Dict[str, float]:
    r = returns.dropna().values
    n = len(r)
    mu_daily = float(np.mean(r))
    sigma_daily = float(np.std(r, ddof=1))
    ann_mu = mu_daily * 252.0 + 0.5 * (sigma_daily ** 2) * 252.0
    ann_vol = sigma_daily * np.sqrt(252.0)
    
    # Log-likelihood normal
    ll = float(np.sum(stats.norm.logpdf(r, loc=mu_daily, scale=sigma_daily)))
    k = 2  # mu, sigma
    aic = 2 * k - 2 * ll
    bic = k * np.log(n) - 2 * ll
    
    return {
        "mu_annual": ann_mu,
        "sigma_annual": ann_vol,
        "mu_daily": mu_daily,
        "sigma_daily": sigma_daily,
        "log_likelihood": ll,
        "aic": aic,
        "bic": bic,
        "n_obs": n,
    }


def simulate_gbm(
    spot: float,
    params: Dict[str, float],
    horizon_days: int = 10,
    n_paths: int = 5000,
    seed: int = 42,
) -> SimulationResult:
    np.random.seed(seed)
    dt = 1.0 / 252.0
    mu = params["mu_annual"]
    sigma = params["sigma_annual"]
    
    # Exact step: S_{t+dt} = S_t * exp((mu - 0.5 * sigma^2)*dt + sigma*sqrt(dt)*Z)
    drift = (mu - 0.5 * (sigma ** 2)) * dt
    diffusion = sigma * np.sqrt(dt)
    
    shocks = np.random.normal(0, 1, size=(n_paths, horizon_days))
    log_increments = drift + diffusion * shocks
    
    cum_log = np.hstack([np.zeros((n_paths, 1)), np.cumsum(log_increments, axis=1)])
    paths = spot * np.exp(cum_log)
    
    terminal_prices = paths[:, -1]
    pct_changes = (terminal_prices - spot) / spot
    
    # Quantiles
    pcts = {p: np.percentile(paths, p, axis=0) for p in [10, 25, 50, 75, 90]}
    
    sim_mean = float(np.mean(terminal_prices))
    theo_mean = float(spot * np.exp(mu * (horizon_days * dt)))
    se = float(np.std(terminal_prices, ddof=1) / np.sqrt(n_paths))
    
    # VaR & CVaR (pérdidas positivas en porcentaje del spot)
    losses = -pct_changes
    var_95 = float(np.percentile(losses, 95))
    var_99 = float(np.percentile(losses, 99))
    cvar_95 = float(np.mean(losses[losses >= var_95]))
    cvar_99 = float(np.mean(losses[losses >= var_99]))
    
    time_grid = np.arange(horizon_days + 1)
    
    return SimulationResult(
        model_name="Movimiento Browniano Geométrico (GBM)",
        ticker="ASSET",
        spot=spot,
        horizon_days=horizon_days,
        n_paths=n_paths,
        time_grid=time_grid,
        paths=paths,
        percentiles=pcts,
        simulated_mean=sim_mean,
        theoretical_mean=theo_mean,
        std_error=se,
        var_95=var_95,
        var_99=var_99,
        cvar_95=cvar_95,
        cvar_99=cvar_99,
        parameters=params,
        log_likelihood=params["log_likelihood"],
        aic=params["aic"],
        bic=params["bic"],
    )


def calibrate_merton_jump(returns: pd.Series) -> Dict[str, float]:
    r = returns.dropna().values
    n = len(r)
    dt = 1.0 / 252.0
    
    # Calibración robusta inicial por threshold / momentos
    med = np.median(r)
    std_init = np.std(r, ddof=1)
    # Saltos identificados como eventos mayores a 2.5 desviaciones
    jump_mask = np.abs(r - med) > (2.5 * std_init)
    jump_count = int(np.sum(jump_mask))
    
    total_years = max(n / 252.0, 0.5)
    lambda_param = max(jump_count / total_years, 0.5)  # tasa de saltos anuales
    
    if jump_count > 3:
        jump_returns = r[jump_mask]
        mu_j = float(np.mean(jump_returns))
        sigma_j = float(np.std(jump_returns, ddof=1))
        sigma_j = max(sigma_j, 0.01)
    else:
        mu_j = -0.02
        sigma_j = 0.04
        
    diff_returns = r[~jump_mask]
    sigma_diff_daily = float(np.std(diff_returns, ddof=1)) if len(diff_returns) > 10 else std_init
    sigma_annual = sigma_diff_daily * np.sqrt(252.0)
    mu_daily = float(np.mean(diff_returns)) if len(diff_returns) > 10 else float(np.mean(r))
    k_bar = np.exp(mu_j + 0.5 * (sigma_j ** 2)) - 1.0
    mu_annual = mu_daily * 252.0 + lambda_param * k_bar
    
    # Log-verosimilitud bajo mezcla Poisson-Normal (truncada a 8 saltos)
    def merton_loglik(params_vec):
        p_mu, p_sig, p_lam, p_muj, p_sigj = params_vec
        if p_sig <= 1e-4 or p_lam < 0 or p_sigj <= 1e-4:
            return 1e10
        k_b = np.exp(p_muj + 0.5 * (p_sigj ** 2)) - 1.0
        dens = np.zeros_like(r)
        pois_lam = p_lam * dt
        for m in range(8):
            prob_m = stats.poisson.pmf(m, pois_lam)
            mu_m = (p_mu - p_lam * k_b - 0.5 * (p_sig ** 2)) * dt + m * p_muj
            var_m = (p_sig ** 2) * dt + m * (p_sigj ** 2)
            if var_m > 0:
                dens += prob_m * stats.norm.pdf(r, loc=mu_m, scale=np.sqrt(var_m))
        dens = np.maximum(dens, 1e-12)
        return -float(np.sum(np.log(dens)))

    init_guess = [mu_annual, sigma_annual, lambda_param, mu_j, sigma_j]
    try:
        res = optimize.minimize(
            merton_loglik,
            init_guess,
            bounds=[(-0.5, 0.8), (0.05, 1.2), (0.2, 50.0), (-0.3, 0.3), (0.01, 0.4)],
            method="L-BFGS-B",
            options={"maxiter": 60},
        )
        if res.success:
            mu_annual, sigma_annual, lambda_param, mu_j, sigma_j = res.x
            ll = -float(res.fun)
        else:
            ll = -merton_loglik(init_guess)
    except Exception:
        ll = -merton_loglik(init_guess)
        
    k = 5  # mu, sigma, lambda, mu_j, sigma_j
    aic = 2 * k - 2 * ll
    bic = k * np.log(n) - 2 * ll
    
    return {
        "mu_annual": float(mu_annual),
        "sigma_annual": float(sigma_annual),
        "lambda": float(lambda_param),
        "mu_j": float(mu_j),
        "sigma_j": float(sigma_j),
        "k_bar": float(np.exp(mu_j + 0.5 * (sigma_j ** 2)) - 1.0),
        "jump_count": float(jump_count),
        "log_likelihood": float(ll),
        "aic": float(aic),
        "bic": float(bic),
        "n_obs": n,
    }


def simulate_merton_jump(
    spot: float,
    params: Dict[str, float],
    horizon_days: int = 10,
    n_paths: int = 5000,
    seed: int = 42,
) -> SimulationResult:
    np.random.seed(seed)
    dt = 1.0 / 252.0
    mu = params["mu_annual"]
    sigma = params["sigma_annual"]
    lam = params["lambda"]
    mu_j = params["mu_j"]
    sigma_j = params["sigma_j"]
    k_bar = params.get("k_bar", np.exp(mu_j + 0.5 * (sigma_j ** 2)) - 1.0)
    
    drift_dt = (mu - lam * k_bar - 0.5 * (sigma ** 2)) * dt
    diff_dt = sigma * np.sqrt(dt)
    
    # Simulación Monte Carlo
    paths = np.zeros((n_paths, horizon_days + 1))
    paths[:, 0] = spot
    
    # Número de saltos Poisson en cada paso
    jump_counts = np.random.poisson(lam * dt, size=(n_paths, horizon_days))
    normal_shocks = np.random.normal(0, 1, size=(n_paths, horizon_days))
    
    # Log-incrementos
    log_inc = drift_dt + diff_dt * normal_shocks
    
    # Sumar saltos donde correspondan
    mask_jumps = jump_counts > 0
    if np.any(mask_jumps):
        # Para cada celda con saltos
        for p_idx, t_idx in zip(*np.where(mask_jumps)):
            m = jump_counts[p_idx, t_idx]
            jump_size = np.sum(np.random.normal(mu_j, sigma_j, size=m))
            log_inc[p_idx, t_idx] += jump_size
            
    cum_log = np.hstack([np.zeros((n_paths, 1)), np.cumsum(log_inc, axis=1)])
    paths = spot * np.exp(cum_log)
    
    terminal_prices = paths[:, -1]
    pct_changes = (terminal_prices - spot) / spot
    pcts = {p: np.percentile(paths, p, axis=0) for p in [10, 25, 50, 75, 90]}
    
    sim_mean = float(np.mean(terminal_prices))
    theo_mean = float(spot * np.exp(mu * (horizon_days * dt)))
    se = float(np.std(terminal_prices, ddof=1) / np.sqrt(n_paths))
    
    losses = -pct_changes
    var_95 = float(np.percentile(losses, 95))
    var_99 = float(np.percentile(losses, 99))
    cvar_95 = float(np.mean(losses[losses >= var_95]))
    cvar_99 = float(np.mean(losses[losses >= var_99]))
    
    time_grid = np.arange(horizon_days + 1)
    
    return SimulationResult(
        model_name="Modelo de Salto de Merton (Jump Diffusion)",
        ticker="ASSET",
        spot=spot,
        horizon_days=horizon_days,
        n_paths=n_paths,
        time_grid=time_grid,
        paths=paths,
        percentiles=pcts,
        simulated_mean=sim_mean,
        theoretical_mean=theo_mean,
        std_error=se,
        var_95=var_95,
        var_99=var_99,
        cvar_95=cvar_95,
        cvar_99=cvar_99,
        parameters=params,
        log_likelihood=params["log_likelihood"],
        aic=params["aic"],
        bic=params["bic"],
    )


def calibrate_ornstein_uhlenbeck(prices: pd.Series) -> Dict[str, float]:
    p = prices.dropna().values
    n = len(p)
    dt = 1.0 / 252.0
    
    # Trabajamos en escala logarítmica X_t = ln(S_t) para garantizar positividad en precios
    x = np.log(p)
    x_t = x[:-1]
    x_next = x[1:]
    
    # Regresión AR(1): X_{t+1} = a + b * X_t + eps
    res = stats.linregress(x_t, x_next)
    b = float(res.slope)
    a = float(res.intercept)
    r_val = float(res.rvalue)
    
    residuals = x_next - (a + b * x_t)
    sigma_eps = float(np.std(residuals, ddof=2))
    
    # Si b < 1, existe reversión a la media
    if 0 < b < 0.9999:
        theta = -np.log(b) / dt
        mu_ou = a / (1.0 - b)
        denom = 1.0 - np.exp(-2 * theta * dt)
        sigma_ou = sigma_eps * np.sqrt(2 * theta / max(denom, 1e-8))
        half_life = np.log(2) / theta * 252.0  # en días hábiles
    else:
        # Regularización suave si no hay reversión estricta
        theta = 0.35  # reversión lenta por defecto
        mu_ou = float(np.mean(x))
        sigma_ou = sigma_eps * np.sqrt(252.0)
        half_life = 999.0
        b = np.exp(-theta * dt)
        a = mu_ou * (1.0 - b)
        
    # Log-verosimilitud del proceso AR(1) Gaussiano
    var_cond = (sigma_ou ** 2) / (2 * theta) * (1.0 - np.exp(-2 * theta * dt))
    var_cond = max(var_cond, 1e-10)
    ll = float(np.sum(stats.norm.logpdf(x_next, loc=(x_t * b + a), scale=np.sqrt(var_cond))))
    
    k = 3  # theta, mu_ou, sigma_ou
    aic = 2 * k - 2 * ll
    bic = k * np.log(n) - 2 * ll
    
    return {
        "theta": float(theta),
        "mu_ou": float(mu_ou),
        "mu_ou_price": float(np.exp(mu_ou)),
        "sigma_ou": float(sigma_ou),
        "half_life_days": float(half_life),
        "slope_b": float(b),
        "intercept_a": float(a),
        "log_likelihood": float(ll),
        "aic": float(aic),
        "bic": float(bic),
        "n_obs": n,
    }


def simulate_ornstein_uhlenbeck(
    spot: float,
    params: Dict[str, float],
    horizon_days: int = 10,
    n_paths: int = 5000,
    seed: int = 42,
) -> SimulationResult:
    np.random.seed(seed)
    dt = 1.0 / 252.0
    theta = params["theta"]
    mu_ou = params["mu_ou"]
    sigma_ou = params["sigma_ou"]
    
    decay = np.exp(-theta * dt)
    cond_var = (sigma_ou ** 2) / (2 * theta) * (1.0 - np.exp(-2 * theta * dt))
    cond_std = np.sqrt(max(cond_var, 1e-10))
    mean_term = mu_ou * (1.0 - decay)
    
    log_spot = np.log(spot)
    log_paths = np.zeros((n_paths, horizon_days + 1))
    log_paths[:, 0] = log_spot
    
    shocks = np.random.normal(0, 1, size=(n_paths, horizon_days))
    
    for t in range(horizon_days):
        log_paths[:, t + 1] = log_paths[:, t] * decay + mean_term + cond_std * shocks[:, t]
        
    paths = np.exp(log_paths)
    terminal_prices = paths[:, -1]
    pct_changes = (terminal_prices - spot) / spot
    pcts = {p: np.percentile(paths, p, axis=0) for p in [10, 25, 50, 75, 90]}
    
    sim_mean = float(np.mean(terminal_prices))
    theo_mean = float(np.exp(log_spot * np.exp(-theta * horizon_days * dt) + mu_ou * (1 - np.exp(-theta * horizon_days * dt)) + 0.5 * cond_var))
    se = float(np.std(terminal_prices, ddof=1) / np.sqrt(n_paths))
    
    losses = -pct_changes
    var_95 = float(np.percentile(losses, 95))
    var_99 = float(np.percentile(losses, 99))
    cvar_95 = float(np.mean(losses[losses >= var_95]))
    cvar_99 = float(np.mean(losses[losses >= var_99]))
    
    time_grid = np.arange(horizon_days + 1)
    
    return SimulationResult(
        model_name="Modelo Ornstein-Uhlenbeck (Reversión a la Media)",
        ticker="ASSET",
        spot=spot,
        horizon_days=horizon_days,
        n_paths=n_paths,
        time_grid=time_grid,
        paths=paths,
        percentiles=pcts,
        simulated_mean=sim_mean,
        theoretical_mean=theo_mean,
        std_error=se,
        var_95=var_95,
        var_99=var_99,
        cvar_95=cvar_95,
        cvar_99=cvar_99,
        parameters=params,
        log_likelihood=params["log_likelihood"],
        aic=params["aic"],
        bic=params["bic"],
    )