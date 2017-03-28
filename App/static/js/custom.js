
$("#answertext").hide();
$(".comment_elements").hide();

$("#answer_button").click(function(){
    $("#answertext").toggle();
});

$(".comment_button").click(function(){
    $(".comment_elements").toggle();
});

$('#questionarea').bind("keyup keypress propertychange", function(){
    var length = $("#questionarea").val().length;
    if($("#questionarea").val() == "") length = 0;
    $("#askCharacterAmount").text("Character Amount: " + length);
});

var scrolling = false;

var scrollLeft = function(num){
    if(scrolling) return;
    scrolling = true;
    var scroll = Math.floor(($("#scroll-"+num).width()/200)) * 200;
    $("#scroll-"+ num).animate({scrollLeft: $("#scroll-" + num).scrollLeft() - scroll}, "1000", "swing", function(){
        scrolling = false;
    });
};

var scrollRight = function(num){
    if(scrolling) return;
    scrolling = true;
    var scroll = Math.floor(($("#scroll-"+num).width()/200)) * 200;
    $("#scroll-"+num).animate({scrollLeft: $("#scroll-"+num).scrollLeft() + scroll}, "1000", "swing", function(){
        scrolling = false;
    });
};

$("#left-scroll-1").click(function(){ scrollLeft(1) });
$("#right-scroll-1").click(function(){ scrollRight(1) });

$("#createQuestionText").show();
$("#createDiscussionText").hide();
$("#createAssignment").hide();

$(".questionTab").click(function(){
    $("#createQuestionText").show();
    $("#createDiscussionText").hide();
    $("#createAssignment").hide();
})

$(".discussionTab").click(function(){
    $("#createQuestionText").hide();
    $("#createDiscussionText").show();
    $("#createAssignment").hide();
})

$(".assignmentTab").click(function(){
    $("#createQuestionText").hide();
    $("#createDiscussionText").hide();
    $("#createAssignment").show();
})


var schools = ['South Elgin High School', 'Bartlett High School', 'Kenyon Woods'];
//$("#school").autocomplete({
//    lookup: schools,
//});

function init(){
    if(document.getElementById("school_name") == null) return;
    var map = document.getElementById("school_view")
    var schoolName = document.getElementById("school_name").textContent
    var schoolState = document.getElementById("school_state").textContent
    
    var mapOptions = {
        center: new google.maps.LatLng(44.5403, -78.5463),
        zoom: 15,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        draggable: false,
        disableDefaultUI: true
    }
    
    var googleMap = new google.maps.Map(map, mapOptions)
    console.log(schoolName + ", " + schoolState);
    (new google.maps.Geocoder()).geocode({'address': schoolName + ", " + schoolState}, function(results, status) {
        if (status === google.maps.GeocoderStatus.OK) {
            googleMap.setCenter(results[0].geometry.location);
            var marker = new google.maps.Marker({
                map: googleMap,
                position: results[0].geometry.location
            });
        } else {
            google.maps.Geocoder().geocode({'address': schoolState}, function(results, status) {
                if (status === google.maps.GeocoderStatus.OK) {
                    googleMap.setCenter(results[0].geometry.location);
                    googleMap.setZoom(5);
                }
            });   
        }
    });
    
}
if ($("school_view") !== null)
    google.maps.event.addDomListener(window, 'load', init);  

$(".school_class").width($(".container").width()/6)
$(".school_class").height($(".container").width()/6)

$("#home-body").ready(function(){
    $(".footer").ready(function(){
        if(document.getElementById("home-body") !== null)
            $(".footer").remove()
    })
});

$(document).ready(function() {
    $('.hidden-group').hide();
    $('#all-questions').show();
    $('#select').change(function() {
        $('.hidden-group').hide();
        console.log($(this).val());
        $('#'+$(this).val()).show();
    });
});
var chillColors = ["#FF0000", "#0F0000", "#0F00F0", "#0FF000", "#FFF000", "#000FFF", "#00FFFF", "#0FF000", "#F0F0F0", "#FFFF0F", "#FFFFF0", "#FFF0FF", "#00000F", ]
var createCircle = function(parent, randomHeight, h){
    var circle = document.createElement("div");
    var width = Math.random () * $(parent).width()/4 +10;
    var height = (randomHeight) ? Math.random() * (h * 1.25) : h;
    $(circle).css({
        "position": "absolute",
        "width": (width) + "px",
        "height": (width) + "px",
        "left": (Math.random() * $(parent).width() - 10) + "px",
        "top": height + "px",
        "z-index": "-1",
        "border-radius": "50%",
        "opacity": "0.4",
        "background-color": chillColors [Math.floor (Math.random () * chillColors.length)]
        //color
    });
    
    $(parent).append(circle);
    
    $(circle).animate({ "top": "-500"}, Math.random() * 10000 + 15000, function(){
        //completed animation create another thingy
        createCircle(parent, false, h);
        $(circle).remove()
    })
};

$("#clask-home").ready(function(){
    $("#clask-home").css({
        "overflow": "hidden"
    });
    for(var i = 0; i < 30; i++){
        createCircle($("#clask-home"), true, $(document).height());
    }
});


$('#school').ready(function() {
    $('#school').autocomplete({
        source: '/api/get_schools/',
        minlength: 2,
    });
});