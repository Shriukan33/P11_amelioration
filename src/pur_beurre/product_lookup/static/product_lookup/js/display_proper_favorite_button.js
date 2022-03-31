function toggle_save_button(id) {
    $('#product_add_' + id).toggleClass('d-none');
    $('#product_remove_' + id).toggleClass('d-flex');
}

// favorites_id_list comes from context
var favorites = JSON.parse(favorites_id_list.textContent);
// Toggles the favorite button to the proper state on page load
for (let id of favorites) {
    if ($('#product_add_' + id).length) {
        $('#product_add_' + id).toggleClass('d-none');
        $('#product_remove_' + id).toggleClass('d-flex');
    }
}

// Add an events on all save btns to handle the click on it.
all_save_buttons = document.getElementsByClassName('save-btn');
for (let button of all_save_buttons) {
    button.addEventListener('click', function(event) {
        /// Parse the class name to get the ID of the item
        var id = this.id.split('_')[2];
        add_to_favorites(id);
    });
}
