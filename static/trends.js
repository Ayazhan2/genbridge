// 1. Ask the backend for all jobs (GET /api/jobs)
fetch("/api/jobs")
  .then(response => response.json())          // 2. Turn the answer (JSON text) into JavaScript objects
  .then(jobs => {
    // 3. Split the jobs into two groups
    const growing = jobs.filter(job => job.trend === "growing");
    const declining = jobs.filter(job => job.trend === "declining");
    showList("growing", growing);
    showList("declining", declining);
  })
  .catch(() => {
    document.getElementById("growing").innerHTML = "<li>Could not load data.</li>";
  });

// 4. Put a list of jobs into the page. Rank 1 gets the longest bar.
function showList(elementId, jobs) {
  const list = document.getElementById(elementId);
  list.innerHTML = "";
  jobs.forEach(job => {
    const width = 100 - (job.rank - 1) * 3;          // 100%, 97%, 94% ...
    const item = document.createElement("li");
    item.innerHTML =
      `<span class="bar" style="width:${width}%"></span>` +
      `<span class="label">${job.title}</span>`;
    list.appendChild(item);
  });
}
