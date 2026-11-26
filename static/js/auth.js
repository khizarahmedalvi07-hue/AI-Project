document.addEventListener("DOMContentLoaded", function () {
    const signupForm = document.getElementById("signup-form");
    const loginForm = document.getElementById("login-form");
    const onboardingForm = document.getElementById("onboarding-form");
    const alertBox = document.getElementById("alert-box");

    function showError(msg) {
        if (!alertBox) return;
        alertBox.textContent = msg;
        alertBox.style.display = "block";
    }

    if (signupForm) {
        signupForm.addEventListener("submit", async function (e) {
            e.preventDefault();
            const payload = {
                full_name: document.getElementById("full_name").value,
                email: document.getElementById("email").value,
                password: document.getElementById("password").value
            };

            const res = await fetch("/api/auth/signup", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await res.json();

            if (res.ok) {
                window.location.href = data.redirect;
            } else {
                showError(data.message || "Sign up failed.");
            }
        });
    }

    if (loginForm) {
        loginForm.addEventListener("submit", async function (e) {
            e.preventDefault();
            const payload = {
                email: document.getElementById("email").value,
                password: document.getElementById("password").value
            };

            const res = await fetch("/api/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await res.json();

            if (res.ok) {
                window.location.href = data.redirect;
            } else {
                showError(data.message || "Login failed.");
            }
        });
    }

    if (onboardingForm) {
        onboardingForm.addEventListener("submit", async function (e) {
            e.preventDefault();
            const payload = {
                age: parseInt(document.getElementById("age").value, 10),
                gender: document.getElementById("gender").value,
                height_cm: parseFloat(document.getElementById("height_cm").value),
                weight_kg: parseFloat(document.getElementById("weight_kg").value),
                goal: document.getElementById("goal").value,
                gym_access: document.getElementById("gym_access").value === "1",
                activity_level: parseFloat(document.getElementById("activity_level").value)
            };

            const res = await fetch("/api/profile", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await res.json();

            if (res.ok) {
                window.location.href = data.redirect;
            } else {
                showError(data.message || "Failed to save profile.");
            }
        });
    }
});