import marimo

__generated_with = "0.20.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    import sample

    return mo, np, plt, sample


@app.cell
def _(mo):
    from textwrap import dedent

    mo.md(
        dedent(
            """
            # Marimo Notebook Demo

            This demo generates synthetic polynomial data, fits a polynomial with
            `numpy.polyfit`, and runs quick checks for arithmetic helpers in
            `sample`.
            """
        )
    )
    return


@app.cell
def _(mo):
    is_script_mode = mo.app_meta().mode == "script"
    return (is_script_mode,)


@app.cell
def _(is_script_mode, mo):
    mode_label = "script" if is_script_mode else "interactive"
    mo.md(f"Current mode: `{mode_label}`")
    return


@app.cell
def _(mo):
    degree = mo.ui.slider(start=1, stop=6, step=1, value=3, label="Fit degree")
    noise = mo.ui.slider(start=0.0, stop=2.0, step=0.05, value=0.4, label="Noise std")
    n_points = mo.ui.slider(start=20, stop=200, step=10, value=80, label="Points")
    seed = mo.ui.slider(start=0, stop=99, step=1, value=7, label="Seed")

    mo.md(f"{degree}\n\n{noise}\n\n{n_points}\n\n{seed}")
    return degree, n_points, noise, seed


@app.cell
def _(degree, n_points, noise, np, seed):
    x = np.linspace(-3.0, 3.0, n_points.value)
    y_true = 0.6 * x**3 - 1.2 * x**2 + 0.8 * x + 2.0
    rng = np.random.default_rng(seed.value)
    y_obs = y_true + rng.normal(loc=0.0, scale=noise.value, size=x.shape)

    coeffs = np.polyfit(x, y_obs, deg=degree.value)
    y_fit = np.polyval(coeffs, x)
    rmse = float(np.sqrt(np.mean((y_obs - y_fit) ** 2)))
    return coeffs, rmse, x, y_fit, y_obs, y_true


@app.cell
def _(coeffs, mo, rmse):
    coeffs_text = ", ".join(f"{c:.4f}" for c in coeffs)
    mo.md(
        f"**Fitted coefficients (highest power first):** `{coeffs_text}`\n\n"
        f"**RMSE on observed data:** `{rmse:.4f}`"
    )
    return


@app.cell
def _(plt, x, y_fit, y_obs, y_true):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.scatter(x, y_obs, s=20, alpha=0.7, label="Observed data")
    ax.plot(x, y_true, linewidth=2, label="True polynomial")
    ax.plot(x, y_fit, linewidth=2, label="Fitted polynomial")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Polynomial fit on synthetic data")
    ax.legend()
    ax.grid(alpha=0.25)
    fig
    return


@app.cell
def _(sample):
    arithmetic_results = {
        "add(2, 3)": sample.add(2, 3),
        "sub(7, 4)": sample.sub(7, 4),
        "mul(6, 5)": sample.mul(6, 5),
        "div(8, 2)": sample.div(8, 2),
    }

    assert arithmetic_results["add(2, 3)"] == 5
    assert arithmetic_results["sub(7, 4)"] == 3
    assert arithmetic_results["mul(6, 5)"] == 30
    assert arithmetic_results["div(8, 2)"] == 4

    div_zero_ok = False
    try:
        sample.div(1, 0)
    except ValueError:
        div_zero_ok = True
    assert div_zero_ok

    return (arithmetic_results,)


@app.cell
def _(arithmetic_results, mo):
    rows = "\n".join(f"- `{expr}` -> `{value}`" for expr, value in arithmetic_results.items())
    mo.md(
        "## sample module checks\n\n"
        "The `sample` module is the reusable package under `src/sample/`. "
        "In this notebook we call its basic arithmetic helpers and verify the "
        "expected behavior, including divide-by-zero handling.\n\n"
        f"{rows}\n\n"
        "- `div(1, 0)` raises `ValueError` as expected"
    )
    return


if __name__ == "__main__":
    app.run()
