import API from "./api";

export function isAuthenticated() {
  const token = localStorage.getItem("token");
  if (!token) return false;

  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.exp * 1000 > Date.now();
  } catch {
    return false;
  }
}

export async function logout() {
  const refresh = localStorage.getItem("refresh_token");

  if (refresh) {
    try {
      await API.post("/auth/logout/", { refresh });
    } catch {
      // best-effort: still clear local session even if the blacklist call fails
    }
  }

  localStorage.removeItem("token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("log_id");
}
