// 훈민정음학회 홈페이지 Worker
// 정적 파일(_site)은 Cloudflare가 직접 서빙하고, 이 스크립트는
// 관리 화면(/admin)의 GitHub 로그인(OAuth)만 처리한다.
//   /auth     → GitHub 로그인 화면으로 보냄
//   /callback → GitHub가 돌려준 코드를 토큰으로 바꿔 관리 화면에 전달
// 그 밖의 모든 주소는 정적 파일로 넘긴다.

const GH_AUTHORIZE = "https://github.com/login/oauth/authorize";
const GH_TOKEN = "https://github.com/login/oauth/access_token";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/auth") return handleAuth(url, env);
    if (url.pathname === "/callback") return handleCallback(url, env);
    return env.ASSETS.fetch(request);
  },
};

function handleAuth(url, env) {
  if (!env.GITHUB_CLIENT_ID) {
    return new Response("GITHUB_CLIENT_ID가 설정되지 않았습니다.", { status: 500 });
  }
  const authUrl = new URL(GH_AUTHORIZE);
  authUrl.searchParams.set("client_id", env.GITHUB_CLIENT_ID);
  authUrl.searchParams.set("redirect_uri", `${url.origin}/callback`);
  authUrl.searchParams.set("scope", "repo,user");
  authUrl.searchParams.set("state", crypto.randomUUID());
  return Response.redirect(authUrl.toString(), 302);
}

async function handleCallback(url, env) {
  const code = url.searchParams.get("code");
  if (!code) return renderResult("error", { error: "코드가 없습니다." });
  let data;
  try {
    const res = await fetch(GH_TOKEN, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        "User-Agent": "scripta-cms",
      },
      body: JSON.stringify({
        client_id: env.GITHUB_CLIENT_ID,
        client_secret: env.GITHUB_CLIENT_SECRET,
        code,
      }),
    });
    data = await res.json();
  } catch (e) {
    return renderResult("error", { error: "GitHub 통신 오류" });
  }
  if (data.access_token) {
    return renderResult("success", { token: data.access_token, provider: "github" });
  }
  return renderResult("error", { error: data.error_description || "토큰을 받지 못했습니다." });
}

function renderResult(status, content) {
  const message = "authorization:github:" + status + ":" + JSON.stringify(content);
  const body =
    "<!doctype html><html><head><meta charset=\"utf-8\"><title>로그인</title></head>" +
    "<body style=\"font-family:sans-serif;padding:2rem;color:#333\">" +
    "<p>로그인 처리 중… 이 창은 곧 닫힙니다.</p>" +
    "<script>(function(){var msg=" +
    JSON.stringify(message) +
    ";function receive(e){window.opener&&window.opener.postMessage(msg,e.origin);}" +
    "window.addEventListener('message',receive,false);" +
    "window.opener&&window.opener.postMessage('authorizing:github','*');})();</script>" +
    "</body></html>";
  return new Response(body, {
    headers: { "Content-Type": "text/html; charset=utf-8" },
  });
}
