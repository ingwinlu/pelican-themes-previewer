function FadeInOnScroll(ObjectList){
    ObjectList.each(function(i) {
        var bottom_of_object = $(this).position().top + $(this).outerHeight();
        var bottom_of_window = $(window).scrollTop() + $(window).height();
        
        if( bottom_of_window > bottom_of_object ){
            $(this).fadeTo(750,1);
        }
    });
}

function loadArticle(index){
    var url = '/index' + index + '.html';
    $.ajax({
        url: url,
        success: function (data) { $('#content').append(data); },
        error: function (request, status, error) {
            alert(request.responseText);
        },
        dataType: 'html'
    });
    return index+1
}

/*setup start index dependend on current url

currentIndex = 2
currenetIndex = loadArticle(currentIndex)*/