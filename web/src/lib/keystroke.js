/**
 * keystroke.js  -  real keystroke-dynamics capture in the browser.
 *
 * Records key-down / key-up times while a target phrase is typed and
 * derives the same feature family the KOTTU dataset uses:
 *
 *   H  (hold)       key-up  - key-down   for each key
 *   DD (down-down)  key-down[n] - key-down[n-1]
 *   UD (up-down)    key-down[n] - key-up[n-1]
 *
 * Attach with `new KeystrokeCapture(inputEl, targetString, onUpdate)`.
 */
export class KeystrokeCapture {
  constructor(input, target, onUpdate) {
    this.input = input;
    this.target = target;
    this.onUpdate = onUpdate || (() => {});
    this.reset();

    this._down = (e) => this._onDown(e);
    this._up = (e) => this._onUp(e);
    input.addEventListener("keydown", this._down);
    input.addEventListener("keyup", this._up);
  }

  reset() {
    this.downs = [];
    this.ups = [];
    this.holds = [];
    this.onUpdate && this.onUpdate(this.snapshot());
  }

  destroy() {
    this.input.removeEventListener("keydown", this._down);
    this.input.removeEventListener("keyup", this._up);
  }

  _printable(e) {
    return e.key.length === 1 || e.key === "Enter";
  }

  _onDown(e) {
    if (!this._printable(e) || e.repeat) return;
    // a fresh run once the field was cleared
    if (this.input.value.length === 0) this.reset();
    this.downs.push(performance.now());
    this.onUpdate(this.snapshot());
  }

  _onUp(e) {
    if (!this._printable(e)) return;
    const t = performance.now();
    this.ups.push(t);
    const i = this.ups.length - 1;
    if (this.downs[i] != null) this.holds[i] = t - this.downs[i];
    this.onUpdate(this.snapshot());
  }

  /** normalised 0..1 bar heights, one per expected key (for the trace) */
  snapshot() {
    const n = this.target.length;
    const flights = [];
    for (let i = 1; i < this.downs.length; i++) {
      flights.push(this.downs[i] - this.downs[i - 1]);
    }
    const all = [...this.holds, ...flights].filter((x) => x > 0);
    const max = all.length ? Math.max(...all) : 1;

    const bars = [];
    for (let i = 0; i < n; i++) {
      const h = this.holds[i];
      const f = i > 0 ? flights[i - 1] : null;
      const v = h != null ? h : f;
      bars.push(v != null ? Math.max(0.06, Math.min(1, v / max)) : 0);
    }
    return {
      bars,
      typedCount: this.downs.length,
      complete: this.downs.length >= n,
      holds: this.holds.slice(),
      flights,
    };
  }
}
