document.addEventListener("DOMContentLoaded", function () {

    function toggleOptions(row) {
        const fieldType = row.querySelector("select[name$='field_type']");
        const optionsField = row.querySelector("textarea[name$='options']")?.closest(".form-row");

        if (!fieldType || !optionsField) return;

        function update() {
            if (fieldType.value === "SELECT") {
                optionsField.style.display = "";
            } else {
                optionsField.style.display = "none";
            }
        }

        fieldType.addEventListener("change", update);
        update();
    }

    function init() {
        document.querySelectorAll(".dynamic-admissionformfield_set").forEach(toggleOptions);
    }

    init();

    // Handle new inline rows
    document.body.addEventListener("click", function (e) {
        if (e.target.classList.contains("add-row")) {
            setTimeout(init, 300);
        }
    });
});