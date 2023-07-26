
const all_exc_btn = document.querySelector(".all_exc_btn");
const by_muscle_btn = document.querySelector(".by_muscle_btn");
const categories_btn = document.querySelector(".categories_btn");

all_exc_btn.addEventListener('click', function() {
    document.querySelector('#by_muscle_table').style.display = 'none';
    document.querySelector('#category_table').style.display = 'none';
    document.querySelector('#all_exc_table').style.display = 'block';
})

by_muscle_btn.addEventListener('click', function() {    
    document.querySelector('#category_table').style.display = 'none';
    document.querySelector('#all_exc_table').style.display = 'none';
    document.querySelector('#by_muscle_table').style.display = 'block';
})

categories_btn.addEventListener('click', function() {
    document.querySelector('#by_muscle_table').style.display = 'none';
    document.querySelector('#all_exc_table').style.display = 'none';
    document.querySelector('#category_table').style.display = 'block';    
})



const instruction_btns = document.querySelectorAll('.instruction_btn');
const target_btns = document.querySelectorAll('.target_btn');
const equipement_btns = document.querySelectorAll('.equipement_btn');


instruction_btns.forEach(function(btn) {
    btn.addEventListener('click', function() {
        const excIdDiv = btn.parentNode.parentNode
        const siblingBtns = btn.parentNode.children
        const siblingBtnArray = Array.from(siblingBtns)
        
        //remove active tag from all other btns
        siblingBtnArray.forEach(function(sibling) {
            sibling.classList.remove('active');
        });

        //add active tag to this btn
        btn.classList.add('active');


        // hide all sibling divs
        const excDivChildren = Array.from(excIdDiv.children)
        excDivChildren.forEach(function(child) {
            if (child.classList[0] === 'target' ||
                child.classList[0] === 'equipement' ) {

                    child.style.display = 'none';
            }

            //show only this btns div
            if (child.classList[0] === 'instruction') {
                child.style.display = 'block'
            }
        })
               
    })
})

target_btns.forEach(function(btn) {
    btn.addEventListener('click', function() {
        const excIdDiv = btn.parentNode.parentNode
        const siblingBtns = btn.parentNode.children
        const siblingBtnArray = Array.from(siblingBtns)
        
        //remove active tag from all other btns
        siblingBtnArray.forEach(function(sibling) {
            sibling.classList.remove('active');
        });

        //add active tag to this btn
        btn.classList.add('active');


        // hide all sibling divs
        const excDivChildren = Array.from(excIdDiv.children)
        excDivChildren.forEach(function(child) {
            if (child.classList[0] === 'instruction' ||
                child.classList[0] === 'equipement' ) {

                    child.style.display = 'none';
            }

            //show only this btns div
            if (child.classList[0] === 'target') {
                child.style.display = 'block'
            }
        })
               
    })
})

equipement_btns.forEach(function(btn) {
    btn.addEventListener('click', function() {
        const excIdDiv = btn.parentNode.parentNode
        const siblingBtns = btn.parentNode.children
        const siblingBtnArray = Array.from(siblingBtns)
        
        //remove active tag from all other btns
        siblingBtnArray.forEach(function(sibling) {
            sibling.classList.remove('active');
        });

        //add active tag to this btn
        btn.classList.add('active');


        // hide all sibling divs
        const excDivChildren = Array.from(excIdDiv.children)
        excDivChildren.forEach(function(child) {
            if (child.classList[0] === 'instruction' ||
                child.classList[0] === 'target' ) {

                    child.style.display = 'none';
            }

            //show only this btns div
            if (child.classList[0] === 'equipement') {
                child.style.display = 'block'
            }
        })
               
    })
})