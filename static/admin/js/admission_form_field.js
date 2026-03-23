document.addEventListener("DOMContentLoaded", function () {

    if (typeof django === "undefined" || !django.jQuery) {
        console.error("Django jQuery not available");
        return;
    }

    const $ = django.jQuery;

    function toggleOptionsField(row) {

        // ✅ get select inside THIS row
        const fieldType = row.find('select[id$="-field_type"]');

        // ✅ get value correctly
        const value = fieldType.val();

        // ✅ target options column (adjust this selector if needed)
        const optionsField = row.find('.-field_type');
        console.log(optionsField.length);
        console.log("Value:", value);

        if (value === "SELECT") {
            console.log("SHOWING");

            optionsField.css("display", "table-cell");

        } else {
            console.log("HIDING");

           optionsField.css("display", "none");
        }
    }

    function initInline() {
        $('tr.form-row').each(function () {
            toggleOptionsField($(this));
        });
    }

    initInline();

    // ✅ change event
    $(document).on('change', 'select[id$="-field_type"]', function () {
        toggleOptionsField($(this).closest('tr'));
    });

    // ✅ select2 event
    $(document).on('select2:select', 'select[id$="-field_type"]', function () {
        toggleOptionsField($(this).closest('tr'));
    });

    // ✅ new inline row
    $(document).on('formset:added', function (event, $row, formsetName) {
        if (formsetName === 'admissionformfield_set') {
            toggleOptionsField($row);
        }
    });

});
