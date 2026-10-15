"use strict";
const $ = id => document.getElementById(id);
let credential = "";
const messages = {
  registration_unavailable_use_existing_token: "Registration is unavailable for this address. Use your existing token; entering an email cannot recover or replace it.",
  invalid_email: "Enter a valid email address.",
  unauthorized: "This token is invalid or has been revoked.",
  burst_limit: "Too many requests. Please wait before trying again.",
  access_service_unavailable: "Account access is temporarily unavailable. Please try again later.",
  registration_capacity_reached: "The demo has reached its account capacity.",
  owner_token_managed_by_operator: "The owner token is managed by the service operator."
};
function message(text) { $("message").textContent = text; }
async function api(path, options = {}) {
  const response = await fetch(path, {cache: "no-store", credentials: "omit", ...options});
  let data;
  try { data = await response.json(); } catch { throw new Error("Service unavailable. Please try again later."); }
  if (!response.ok) {
    let text = messages[data.error] || (data.error?.includes("limit") ? "The demo allowance has been reached." : "The request could not be completed.");
    const retry = response.headers.get("Retry-After");
    if (retry) text += ` Try again in ${retry} seconds.`;
    throw new Error(text);
  }
  return data;
}
function headers() { return {Authorization: `Bearer ${credential}`}; }
async function showAccount() {
  const data = await api("/api/account", {headers: headers()});
  $("remaining").textContent = `${data.daily_tool_remaining} / ${data.daily_tool_limit}`;
  $("reset").textContent = `Resets ${new Date(data.resets_at).toLocaleString()}`;
  $("shared").textContent = `Shared allowance: ${data.shared_tool_remaining_today} calls today · ${data.shared_tool_remaining_month} this month`;
  $("endpoint").value = location.origin + "/mcp";
  $("entry").hidden = true; $("account").hidden = false;
}
async function action(event, work) {
  event.preventDefault(); message("");
  const buttons = [...document.querySelectorAll("button")];
  buttons.forEach(button => button.disabled = true);
  try { await work(); } catch (error) { message(error.message); }
  finally { buttons.forEach(button => button.disabled = false); }
}
$("register").addEventListener("submit", event => action(event, async () => {
  const data = await api("/api/register", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({email: $("email").value})});
  credential = data.token;
  $("new-token").value = credential; $("issued").hidden = false;
  // Display the one-time token even if the subsequent usage request fails.
  $("entry").hidden = true; $("account").hidden = false;
  $("endpoint").value = location.origin + "/mcp";
  $("email").value = "";
  await showAccount();
}));
$("authorize").addEventListener("submit", event => action(event, async () => {
  credential = $("token").value.trim(); $("token").value = "";
  $("new-token").value = ""; $("issued").hidden = true;
  await showAccount();
}));
$("refresh").addEventListener("click", event => action(event, showAccount));
$("copy").addEventListener("click", event => action(event, async () => {
  await navigator.clipboard.writeText($("new-token").value); message("Token copied. Save it securely.");
}));
function signOut() {
  credential = ""; $("new-token").value = ""; $("token").value = "";
  $("account").hidden = true; $("issued").hidden = true; $("entry").hidden = false;
  $("confirm-revoke").checked = false;
}
$("logout").addEventListener("click", () => { signOut(); message("Signed out. Your saved token still works."); });
$("revoke").addEventListener("click", event => action(event, async () => {
  if (!$("confirm-revoke").checked) throw new Error("Confirm that you understand revocation ends access.");
  await api("/api/revoke", {method: "POST", headers: headers()});
  signOut(); message("Token revoked.");
}));
window.addEventListener("pagehide", signOut);
