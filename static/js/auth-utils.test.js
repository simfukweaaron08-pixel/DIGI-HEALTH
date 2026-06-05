const { normalizeIdentifier, getCookie } = require("./auth-utils");

describe("auth-utils", () => {
  test("normalizeIdentifier trims whitespace", () => {
    expect(normalizeIdentifier("  user@example.com  ")).toBe(
      "user@example.com",
    );
  });

  test("getCookie returns cookie value when present", () => {
    document.cookie = "csrftoken=token";
    document.cookie = "sessionid=abc123";
    expect(getCookie("csrftoken")).toBe("token");
  });

  test("getCookie returns null when cookie is missing", () => {
    document.cookie = "csrftoken=; Max-Age=0";
    document.cookie = "sessionid=abc123";
    expect(getCookie("csrftoken")).toBeNull();
  });
});
