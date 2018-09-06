"use strict";

// FUTURE FEATURE: check to see all pieces processed, 
// then call in callback to show button to go to closet

function flashSaved(result) {
    $(`#form-${result}`).removeClass("visible").addClass("hidden");
    $(`#div-${result}`).removeClass("hidden").addClass("visible");
};

function savePieceDetails(thing) {

    // creates list of all elements in form
    let formInputs= $(`#form-${thing}`).serialize();

    $.ajax({
        type: "POST",
        url: '/verifycloset',
        data: formInputs,
        dataType: "json",
        success: flashSaved(thing)
    });

};

function flashWorn(result) {
    $("#btn-go-home").removeClass("hidden").addClass("visible");
    $("#btn-choose-other-outfit").removeClass("visible").addClass("hidden");
    $("#btn-wear-outfit").html(result)
    $("#btn-wear-outfit").css("background-color", "#b4dbc0");
};

function wearOutfit(outfitjson) {

    let piece_1 = outfitjson['piece_1']['piece_id'];
    let piece_2 = outfitjson['piece_2']['piece_id'];
    let piece_3 = 0;

    if ('piece_3' in outfitjson) {
        piece_3 = outfitjson['piece_3']['piece_id'];
    }

    let outfitData = { 
        "piece_1" : piece_1,
        "piece_2" : piece_2, 
        "piece_3" : piece_3,
        };

    $.post("/ootd", outfitData, flashWorn);
};


