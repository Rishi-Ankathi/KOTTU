/**
 * Client for the KOTTU API.
 *
 * This file used to hold a local simulation; it now calls the FastAPI service.
 * Point it at the deployed API by setting, at build time:
 *
 *     PUBLIC_KOTTU_API=https://<your-space>.hf.space
 *
 * With nothing set it targets a local `uvicorn api.main:app` on :8000.
 */

const _env =
  typeof import.meta !== "undefined" && import.meta.env ? import.meta.env : {};

const BASE = (_env.PUBLIC_KOTTU_API || "http://127.0.0.1:8000").replace(
  /\/+$/,
  ""
);

export const PASSPHRASE = ".tie5Roanl";
export const API_BASE = BASE;

export class ApiError extends Error {
  constructor(message, status, data) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }
}

async function post(path, body) {
  let res;
  try {
    res = await fetch(BASE + path, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(body),
    });
  } catch (e) {
    throw new ApiError("could not reach the API", 0, null);
  }

  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const detail =
      typeof data.detail === "string" ? data.detail : res.statusText;
    throw new ApiError(detail, res.status, data);
  }
  return data;
}

/** {features:[31]} -> {user, confidence} */
export function identify(features) {
  return post("/identify", { features });
}

/** {name, samples:[[31], ...]} -> {name, samples, threshold} */
export function enroll(name, samples) {
  return post("/enroll", { name, samples });
}

/** {name, features:[31]} -> {accepted, distance, threshold, margin} */
export function verify(name, features) {
  return post("/verify", { name, features });
}

/** true if the API answers /health */
export async function health() {
  try {
    const res = await fetch(BASE + "/health", { method: "GET" });
    return res.ok;
  } catch {
    return false;
  }
}
