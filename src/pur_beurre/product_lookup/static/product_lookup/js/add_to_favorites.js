// Function that uses AJAX to add a product to the user's favorites
function add_to_favorites(product_id) {
    var data = {
        'product_id': product_id,
        'csrfmiddlewaretoken': document.getElementsByName("csrfmiddlewaretoken")[0].value
    };
    $.ajax({
        type: 'POST',
        url: '/ajax/toggle-favorite/' + product_id,
        data: data,
    });
    toggle_save_button(product_id);
}
