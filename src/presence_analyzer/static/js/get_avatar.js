(function() {
    $(function() {
        $('#user_id').change(function() {
            var getAvatarUrl = '/api/v1/user_avatar_url/' + $('#user_id').val(),
                $userAvatarElement = $('#user_avatar'),
                intranetBaseUrl = 'https://intranet.stxnext.pl';

            $.getJSON(getAvatarUrl, function(result) {
                $userAvatarElement.attr('src', intranetBaseUrl + result);
            }).fail(function() {
                var $errorSection = $('#error-message'),
                    $selectedUser = $('#user_id').val();

                if($selectedUser) {
                    $userAvatarElement.attr('src', '');
                    $errorSection.text('User details not found.');
                } else{
                    $errorSection.text('');
                }
            });
        });
    });
})(jQuery);
