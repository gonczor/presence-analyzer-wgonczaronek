(function() {
    $(function() {
        $('#user_id').change(function() {
            var getAvatarUrl = '/api/v1/user_avatar_url/' + $('#user_id').val(),
                $userAvatarElement = $('#user_avatar'),
                intranetBaseUrl = 'https://intranet.stxnext.pl',
                $errorSection = $('#error-message');

            $.getJSON(getAvatarUrl, function(result) {
                $errorSection.text('');
                $userAvatarElement.attr('src', intranetBaseUrl + result);
            }).fail(function() {
                var $selectedUser = $('#user_id').val();

                $userAvatarElement.attr('src', '');
                if($selectedUser) {
                    $errorSection.text('User details not found.');
                } else {
                    $errorSection.text('');
                }
            });
        });
    });
})(jQuery);
