/**
 * Turn a recorded keystroke session into the 31 CMU timing features, in the
 * exact column order the model's scaler expects.
 *
 * Passphrase:  . t i e 5 R o a n l  <Enter>  - 11 "units".
 * The capital R needs Shift. Following the CMU benchmark we treat the `r` key
 * itself as the unit and ignore Shift's own down/up for timing (Shift only
 * lengthens the gap into `r`). If live features drift from the dataset, this
 * is the first assumption to revisit - see docs/AUTH_PLAN.md, step B2.
 *
 * Timings are keydown/keyup in milliseconds; output is in SECONDS.
 *   H  (hold)      = up[k]     - down[k]
 *   DD (down-down) = down[k+1] - down[k]
 *   UD (up-down)   = down[k+1] - up[k]      (negative on rollover - keep the sign)
 */

export const PASSPHRASE = ".tie5Roanl";

// unit keys as they arrive from KeyboardEvent.key (letters lower-cased)
export const UNITS = [".", "t", "i", "e", "5", "r", "o", "a", "n", "l", "Enter"];

const MS = 1000;

function normKey(key) {
  return key === "Enter" ? "Enter" : key.length === 1 ? key.toLowerCase() : key;
}

/**
 * @param {{key:string, type:"down"|"up", t:number}[]} events  in arrival order
 * @returns {number[]} 31 features in CMU column order (seconds)
 */
export function extractFeatures(events) {
  const down = {};
  const up = {};

  for (const e of events) {
    const k = normKey(e.key);
    if (!UNITS.includes(k)) continue; // Shift and strays
    if (e.type === "down" && down[k] == null) down[k] = e.t;
    else if (e.type === "up" && up[k] == null) up[k] = e.t;
  }

  for (const u of UNITS) {
    if (down[u] == null || up[u] == null) {
      throw new Error(`incomplete session: missing timing for "${u}"`);
    }
  }

  const f = [];
  for (let k = 0; k < UNITS.length; k++) {
    const cur = UNITS[k];
    f.push((up[cur] - down[cur]) / MS); // H.<cur>
    if (k < UNITS.length - 1) {
      const nxt = UNITS[k + 1];
      f.push((down[nxt] - down[cur]) / MS); // DD.<cur>.<nxt>
      f.push((down[nxt] - up[cur]) / MS); // UD.<cur>.<nxt>
    }
  }
  return f; // length 31
}

/**
 * Wraps a text input: records key events, watches the typed string, and calls
 * `onAttempt(features)` once per clean run of the passphrase + Enter. Any typo
 * or Backspace resets the run.
 */
export class PhraseCapture {
  constructor(input, { onAttempt, onProgress } = {}) {
    this.input = input;
    this.onAttempt = onAttempt || (() => {});
    this.onProgress = onProgress || (() => {});
    this.events = [];

    this._down = (e) => this._on(e, "down");
    this._up = (e) => this._on(e, "up");
    input.addEventListener("keydown", this._down);
    input.addEventListener("keyup", this._up);
  }

  destroy() {
    this.input.removeEventListener("keydown", this._down);
    this.input.removeEventListener("keyup", this._up);
  }

  reset() {
    this.events = [];
    this.input.value = "";
    this.onProgress(0);
  }

  _on(e, type) {
    const key = e.key;

    if (key === "Backspace") {
      this.reset();
      return;
    }
    if (key !== "Enter" && key.length !== 1) return; // Shift, Tab, arrows...

    this.events.push({
      key,
      type,
      t: typeof e.timeStamp === "number" ? e.timeStamp : performance.now(),
    });

    if (type === "up" && key === "Enter") {
      if (this.input.value === PASSPHRASE) {
        try {
          const feats = extractFeatures(this.events);
          this.reset();
          this.onAttempt(feats);
        } catch {
          this.reset();
        }
      } else {
        this.reset();
      }
      return;
    }

    if (type === "up" && key.length === 1) {
      const v = this.input.value;
      if (!PASSPHRASE.startsWith(v)) {
        this.reset();
        return;
      }
      this.onProgress(v.length);
    }
  }
}
