const terminal = document.getElementById("terminal");

fetch("/api/attacks")
  .then(res => res.json())
  .then(data => {

    let attackCount = {};
    data.forEach(row => {
      const line = `[${row.time || "N/A"}] ${row.attack_type} FROM ${row.source_ip}`;
      terminal.innerHTML += line + "<br>";

      attackCount[row.attack_type] =
        (attackCount[row.attack_type] || 0) + 1;
    });

    terminal.scrollTop = terminal.scrollHeight;

    new Chart(document.getElementById("typeChart"), {
      type: "doughnut",
      data: {
        labels: Object.keys(attackCount),
        datasets: [{
          data: Object.values(attackCount),
          backgroundColor: ["red", "orange", "yellow", "purple"]
        }]
      }
    });
  });
