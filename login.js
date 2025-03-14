async function login() {
  const username = document.getElementById("userName").value;
  const password = document.getElementById("password").value;

  if (!username || !password) {
    alert("Du hast nicht alle Felder ausgefüllt!");
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:6060/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }), // Kurzschreibweise für { username: username, password: password }
    });

    if (!response.ok) {
      throw new Error(
        `Login fehlgeschlagen: ${response.status} ${response.statusText}`
      );
    }

    const data = await response.json();
    alert("Erfolgreich eingeloggt!");
  } catch (error) {
    console.error("Fehler:", error);
    alert("Login fehlgeschlagen! Bitte überprüfe deine Eingaben.");
  }
}
