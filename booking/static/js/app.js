document.addEventListener("DOMContentLoaded", () => {
  // 1. Live doctor search: filters the list as the user types, no page reload.
  const search = document.getElementById("live-search");
  if (search) {
    search.addEventListener("input", () => {
      const term = search.value.trim().toLowerCase();
      document.querySelectorAll(".doctor-row").forEach((row) => {
        row.hidden = !row.dataset.search.includes(term);
      });
    });
  }

  // 2. Dynamic slot picker: changing the date fetches that day's open times.
  const slotList = document.getElementById("slot-list");
  const dateInput = document.getElementById("slot-date");
  if (slotList && dateInput) {
    dateInput.addEventListener("change", async () => {
      slotList.textContent = "Loading times…";
      try {
        const response = await fetch(`${slotList.dataset.api}?date=${encodeURIComponent(dateInput.value)}`);
        if (!response.ok) throw new Error(response.status);
        const data = await response.json();
        renderSlots(slotList, data.slots);
      } catch (err) {
        slotList.textContent = "Could not load times. Please try again.";
      }
    });
  }

  // 3. Character counter on the booking form.
  const reason = document.getElementById("id_reason");
  const counter = document.getElementById("reason-count");
  if (reason && counter) {
    const update = () => { counter.textContent = `${reason.value.length}/${reason.maxLength}`; };
    reason.addEventListener("input", update);
    update();
  }

  // 4. Cancel confirmation modal: points the form at the chosen appointment.
  const cancelModal = document.getElementById("cancelModal");
  if (cancelModal) {
    cancelModal.addEventListener("show.bs.modal", (event) => {
      const trigger = event.relatedTarget;
      document.getElementById("cancel-form").action = trigger.dataset.action;
      document.getElementById("cancel-doctor").textContent = trigger.dataset.doctor;
    });
  }
});

function renderSlots(container, slots) {
  container.replaceChildren();
  if (!slots.length) {
    const note = document.createElement("p");
    note.className = "empty";
    note.textContent = "No open times on this date. Try another day.";
    container.appendChild(note);
    return;
  }
  slots.forEach((slot) => {
    const link = document.createElement("a");
    link.className = "slot";
    link.href = slot.url;
    link.textContent = slot.label;
    container.appendChild(link);
  });
}
