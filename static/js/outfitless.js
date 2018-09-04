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
    console.log(result);
};

function wearOutfit(outfitjson) {

    let outfitData= {
        "piece_1": $('#piece_1').val(),
        "piece_2": $('#piece_2').val(),
        "piece_3": $('#piece_3').val(),
    };

    console.log(outfitData);

    $.post('/ootd', outfitData, flashWorn);
};


