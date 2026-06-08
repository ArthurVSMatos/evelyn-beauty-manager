document.addEventListener("submit", (event) => {
    const form = event.target;
    const message = form.dataset.confirm;
    if (message && !window.confirm(message)) {
        event.preventDefault();
    }
});

const serviceSelect = document.querySelector("#service-select");
const amountInput = document.querySelector("#amount-input");

if (serviceSelect && amountInput) {
    serviceSelect.addEventListener("change", () => {
        const selected = serviceSelect.options[serviceSelect.selectedIndex];
        if (selected.dataset.price && !amountInput.value) {
            amountInput.value = Number(selected.dataset.price).toFixed(2);
        }
    });
}

if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
        navigator.serviceWorker.register("/static/service-worker.js");
    });
}
