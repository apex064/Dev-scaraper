function showLoader() {
    document.getElementById("loader").style.display = "block";
}

function showToast(message, isError = false) {
    const toast = document.getElementById("toast");
    toast.innerText = message;
    toast.className = "toast" + (isError ? " error" : "");
    toast.style.opacity = 1;

    setTimeout(() => {
        toast.style.opacity = 0;
    }, 4000);
}

function showTab(id) {
    document.querySelectorAll(".tab-content").forEach(t => t.classList.remove("active"));
    const target = document.getElementById("tab-" + id);
    if (target) target.classList.add("active");
}
