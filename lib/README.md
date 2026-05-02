# lib/

Reserved for future helper scripts shared across skills.

Planned:

- **`log_matrix.py`** — generate the 1.6× logarithmic Power × Scan-Speed matrix used by the DOE skills (per `references/laser_ablation.md` §12).
- **`laser_calc.py`** — focal spot, fluence, peak intensity, Rayleigh range, damage-threshold scaling. Used everywhere.
- **`ppc_writer.py`** — write DOE matrices to Excel with column layouts matching common process-parameter calculator spreadsheets.

Until these exist, skills compute values inline and emit CSV / Markdown tables.
