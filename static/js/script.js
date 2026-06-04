/* ============================================================
   DigiHealth — Authentication Script
   Handles login, registration, logout, and CSRF for Django.
   ============================================================ */

(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", init);

  async function init() {
    await fetchCsrfToken();

    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const logoutBtn = document.getElementById("logoutBtn");

    if (loginForm) {
      setupLoginForm(loginForm);
      setupLoginAnimations();
    }

    if (registerForm) {
      setupRegisterForm(registerForm);
      setupRegisterAnimations();
    }

    if (logoutBtn) {
      logoutBtn.addEventListener("click", handleLogout);
    }
  }

  async function fetchCsrfToken() {
    await fetch("/auth/csrf-token/", {
      method: "GET",
      credentials: "include",
    });
  }

  function setupLoginForm(form) {
    const studentId = document.getElementById("studentId");
    const password = document.getElementById("password");
    const eyeBtn = document.getElementById("eyeBtn");
    const eyeIcon = document.getElementById("eyeIcon");
    const groupId = document.getElementById("groupId");
    const groupPw = document.getElementById("groupPw");
    const idError = document.getElementById("idError");
    const pwError = document.getElementById("pwError");
    const submitBtn = document.getElementById("submitBtn");

    eyeBtn.addEventListener("click", function () {
      const isHidden = password.type === "password";
      password.type = isHidden ? "text" : "password";
      eyeIcon.classList.toggle("fa-eye", !isHidden);
      eyeIcon.classList.toggle("fa-eye-slash", isHidden);
      password.focus();
    });

    studentId.addEventListener("input", function () {
      clearError(groupId, idError);
    });
    password.addEventListener("input", function () {
      clearError(groupPw, pwError);
    });

    form.addEventListener("submit", async function (event) {
      event.preventDefault();

      const identifier = studentId.value.trim();
      const pw = password.value;
      const valid = validateLogin(
        identifier,
        pw,
        groupId,
        idError,
        groupPw,
        pwError,
      );
      if (!valid) return;

      setLoading(submitBtn, true);
      const response = await postJson("/auth/login/", {
        identifier,
        password: pw,
      });
      setLoading(submitBtn, false);

      if (response.ok) {
        window.location.href = "/dashboard/";
        return;
      }

      const payload = await response.json();
      renderFormErrors(payload.errors, {
        identifier: [groupId, idError],
        password: [groupPw, pwError],
      });
    });
  }

  function setupRegisterForm(form) {
    const username = document.getElementById("username");
    const email = document.getElementById("email");
    const password1 = document.getElementById("password1");
    const password2 = document.getElementById("password2");
    const groupUsername = document.getElementById("groupUsername");
    const groupEmail = document.getElementById("groupEmail");
    const groupPw = document.getElementById("groupPw");
    const groupPw2 = document.getElementById("groupPw2");
    const usernameError = document.getElementById("usernameError");
    const emailError = document.getElementById("emailError");
    const password1Error = document.getElementById("password1Error");
    const password2Error = document.getElementById("password2Error");
    const submitBtn = document.getElementById("submitBtn");

    username.addEventListener("input", function () {
      clearError(groupUsername, usernameError);
    });
    email.addEventListener("input", function () {
      clearError(groupEmail, emailError);
    });
    password1.addEventListener("input", function () {
      clearError(groupPw, password1Error);
    });
    password2.addEventListener("input", function () {
      clearError(groupPw2, password2Error);
    });

    form.addEventListener("submit", async function (event) {
      event.preventDefault();

      const name = username.value.trim();
      const emailValue = email.value.trim();
      const pw1 = password1.value;
      const pw2 = password2.value;
      const valid = validateRegister(
        name,
        emailValue,
        pw1,
        pw2,
        groupUsername,
        usernameError,
        groupEmail,
        emailError,
        groupPw,
        password1Error,
        groupPw2,
        password2Error,
      );
      if (!valid) return;

      setLoading(submitBtn, true);
      const response = await postJson("/auth/register/", {
        username: name,
        email: emailValue,
        password1: pw1,
        password2: pw2,
      });
      setLoading(submitBtn, false);

      if (response.ok) {
        window.location.href = "/login/";
        return;
      }

      const payload = await response.json();
      renderFormErrors(payload.errors, {
        username: [groupUsername, usernameError],
        email: [groupEmail, emailError],
        password1: [groupPw, password1Error],
        password2: [groupPw2, password2Error],
      });
    });
  }

  async function handleLogout(event) {
    event.preventDefault();

    const response = await postJson("/auth/logout/", {});
    if (response.ok) {
      window.location.href = "/login/";
      return;
    }

    console.error("Logout failed");
  }

  function validateLogin(
    identifier,
    password,
    groupId,
    idError,
    groupPw,
    pwError,
  ) {
    let valid = true;
    if (!identifier) {
      valid = false;
      showError(groupId, idError, "Please enter your Student ID or email.");
    }

    if (!password) {
      valid = false;
      showError(groupPw, pwError, "Please enter your password.");
    }

    return valid;
  }

  function validateRegister(
    name,
    email,
    pw1,
    pw2,
    groupUsername,
    usernameError,
    groupEmail,
    emailError,
    groupPw,
    password1Error,
    groupPw2,
    password2Error,
  ) {
    let valid = true;
    if (!name) {
      valid = false;
      showError(groupUsername, usernameError, "Choose a username.");
    }

    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      valid = false;
      showError(groupEmail, emailError, "Enter a valid email address.");
    }

    if (!pw1 || pw1.length < 10) {
      valid = false;
      showError(
        groupPw,
        password1Error,
        "Choose a password with at least 10 characters.",
      );
    }

    if (pw1 !== pw2) {
      valid = false;
      showError(groupPw2, password2Error, "Passwords do not match.");
    }

    return valid;
  }

  async function postJson(url, data) {
    return fetch(url, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify(data),
    });
  }

  function renderFormErrors(errors, fieldMap) {
    if (!errors) return;
    Object.keys(fieldMap).forEach(function (field) {
      const entry = fieldMap[field];
      if (!entry || !errors[field]) return;
      showError(entry[0], entry[1], errors[field].join(" "));
    });

    if (errors.__all__) {
      const fallback = Object.values(fieldMap)[0];
      if (fallback) {
        showError(fallback[0], fallback[1], errors.__all__.join(" "));
      }
    }
  }

  function getCookie(name) {
    const value = document.cookie
      .split("; ")
      .find((row) => row.startsWith(name + "="));
    return value ? decodeURIComponent(value.split("=")[1]) : null;
  }

  function showError(group, errorEl, msg) {
    if (!group || !errorEl) return;
    group.classList.add("has-error");
    errorEl.textContent = msg;
    errorEl.classList.add("show");
  }

  function clearError(group, errorEl) {
    if (!group || !errorEl) return;
    group.classList.remove("has-error");
    errorEl.textContent = "";
    errorEl.classList.remove("show");
  }

  function setLoading(button, state) {
    if (!button) return;
    if (state) {
      button.classList.add("loading");
      button.disabled = true;
    } else {
      button.classList.remove("loading");
      button.disabled = false;
    }
  }

  function setupLoginAnimations() {
    const logo = document.getElementById("logo");
    const pageHeading = document.getElementById("pageHeading");
    const groupId = document.getElementById("groupId");
    const groupPw = document.getElementById("groupPw");
    const formRow = document.getElementById("formRow");
    const submitBtn = document.getElementById("submitBtn");
    const helpText = document.getElementById("helpText");
    const infoPanel = document.getElementById("infoPanel");

    if (
      !logo ||
      !pageHeading ||
      !groupId ||
      !groupPw ||
      !formRow ||
      !submitBtn ||
      !helpText ||
      !infoPanel
    ) {
      return;
    }

    gsap.set(
      [logo, pageHeading, groupId, groupPw, formRow, submitBtn, helpText],
      {
        opacity: 0,
        y: 18,
      },
    );

    gsap.set(infoPanel, {
      opacity: 0,
      x: 24,
    });

    gsap
      .timeline({ defaults: { ease: "power3.out" } })
      .to(logo, { opacity: 1, y: 0, duration: 0.5 }, 0.1)
      .to(pageHeading, { opacity: 1, y: 0, duration: 0.5 }, 0.22)
      .to(groupId, { opacity: 1, y: 0, duration: 0.45 }, 0.34)
      .to(groupPw, { opacity: 1, y: 0, duration: 0.45 }, 0.44)
      .to(formRow, { opacity: 1, y: 0, duration: 0.4 }, 0.54)
      .to(submitBtn, { opacity: 1, y: 0, duration: 0.4 }, 0.62)
      .to(helpText, { opacity: 1, y: 0, duration: 0.35 }, 0.72)
      .to(infoPanel, { opacity: 1, x: 0, duration: 0.6 }, 0.3);
  }

  function setupRegisterAnimations() {
    const logo = document.getElementById("logo");
    const pageHeading = document.getElementById("pageHeading");
    const infoPanel = document.getElementById("infoPanel");
    if (!logo || !pageHeading || !infoPanel) {
      return;
    }

    gsap.set([logo, pageHeading], {
      opacity: 0,
      y: 18,
    });

    gsap.set(infoPanel, {
      opacity: 0,
      x: 24,
    });

    gsap
      .timeline({ defaults: { ease: "power3.out" } })
      .to(logo, { opacity: 1, y: 0, duration: 0.5 }, 0.1)
      .to(pageHeading, { opacity: 1, y: 0, duration: 0.5 }, 0.22)
      .to(infoPanel, { opacity: 1, x: 0, duration: 0.6 }, 0.3);
  }
})();
