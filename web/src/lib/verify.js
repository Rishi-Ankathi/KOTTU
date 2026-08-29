/**
 * verify.js  -  the swap point.
 *
 * Right now this returns a DETERMINISTIC SIMULATION seeded by the selected
 * identity + what was typed, so the Authentication screen has a coherent,
 * repeatable result to render. It does not run the model.
 *
 * To make it real later, replace the body of `verify()` with:
 *
 *     const res = await fetch("/api/verify", {
 *       method: "POST",
 *       headers: { "content-type": "application/json" },
 *       body: JSON.stringify({ user: userId, features }),
 *     });
 *     return res.json();
 *
 * ...backed by a thin service that imports src/predict.Predictor. Nothing
 * else on the page has to change - the shape below is the contract.
 */

export const PASSPHRASE = ".tie5Roanl";
export const THRESHOLD = 0.6;

/* string hash -> seeded PRNG (mulberry32) */
function seeded(str) {
  let h = 1779033703 ^ str.length;
  for (let i = 0; i < str.length; i++) {
    h = Math.imul(h ^ str.charCodeAt(i), 3432918353);
    h = (h << 13) | (h >>> 19);
  }
  let a = h >>> 0;
  return function () {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/**
 * @param {string} userId   selected enrolled identity
 * @param {string} typed     what the person typed
 * @param {string[]} users   full enrolled roster
 * @returns {{predicted:string, confidence:number, accepted:boolean,
 *            probabilities:Record<string,number>, typedOk:boolean}}
 */
export function verify(userId, typed, users) {
  const rng = seeded(userId + "|" + typed);
  const typedOk = typed === PASSPHRASE;

  const spread = (top, topProb) => {
    const dist = { [top]: topProb };
    const rest = users.filter((u) => u !== top);
    const w = rest.map(() => rng());
    const wt = w.reduce((a, b) => a + b, 0) || 1;
    rest.forEach((u, i) => (dist[u] = ((1 - topProb) * w[i]) / wt));
    return dist;
  };

  let predicted;
  let confidence;
  let probabilities;

  if (typedOk && rng() < 0.75) {
    // genuine: right phrase, matching rhythm
    predicted = userId;
    confidence = 0.86 + rng() * 0.11;
    probabilities = spread(predicted, confidence);
  } else if (typedOk) {
    // right phrase, rhythm looks like someone else
    const others = users.filter((u) => u !== userId);
    predicted = others[Math.floor(rng() * others.length)];
    confidence = 0.45 + rng() * 0.25;
    probabilities = spread(predicted, confidence);
  } else {
    // wrong phrase: no clear match
    const scores = {};
    let total = 0;
    for (const u of users) {
      const v = Math.pow(rng(), 3);
      scores[u] = v;
      total += v;
    }
    probabilities = {};
    for (const u of users) probabilities[u] = scores[u] / total;
    predicted = Object.keys(probabilities).reduce((a, b) =>
      probabilities[a] > probabilities[b] ? a : b
    );
    confidence = probabilities[predicted];
  }

  const accepted = typedOk && predicted === userId && confidence >= THRESHOLD;
  return { predicted, confidence, accepted, probabilities, typedOk };
}
