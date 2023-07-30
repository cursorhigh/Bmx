$(document).ready(function() {
    var pid = 'player_id_value';
    var oid = 'opponent_id_value';
    var category = 'category_value';
    console.log('Triggering AJAX request...');
    $.ajax({
        url: '/mid/',
        method: 'GET',
        data: {
            pid: pid,
            oid: oid,
            category: category
        },
        success: function(response) {
            console.log('Success callback reached!');
        },
        error: function(xhr, status, error) {
            console.log(error);
        }
    });
});