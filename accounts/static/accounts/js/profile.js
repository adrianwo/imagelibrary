window.addEventListener("load", function () {
    (function ($) {
        var select = $('#id_profile-0-tier'),
            height_1 = $('.field-height_1'),
            height_2 = $('.field-height_2'),
            original_size = $('.field-original_link'),
            generate_link = $('.field-generate_link');

        function toggleCustom(value) {
            if (value === 'Custom') {
                height_1.show();
                height_2.show();
                generate_link.show();
                original_size.show();
            } else {
                height_1.hide();
                height_2.hide();
                generate_link.hide();
                original_size.hide();
            }
        }

        // show/hide on load based on existing value of selectField
        toggleCustom(select.val());

        // show/hide on change
        select.change(function () {
            toggleCustom($(this).val());
        });
    })(django.jQuery);
});