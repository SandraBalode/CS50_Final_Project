
const all_exc_btn = document.querySelector(".all_exc_btn");
const by_muscle_btn = document.querySelector(".by_muscle_btn");
const categories_btn = document.querySelector(".categories_btn");

all_exc_btn.addEventListener('click', function() {
    document.querySelector('#by_muscle_table').style.display = 'none';
    document.querySelector('#all_exc_table').style.display = 'block';

    if (document.querySelector('#category_table')) {
        document.querySelector('#category_table').style.display = 'none';
    }
})

by_muscle_btn.addEventListener('click', function() {        
    document.querySelector('#all_exc_table').style.display = 'none';
    document.querySelector('#by_muscle_table').style.display = 'block';

    if (document.querySelector('#category_table')) {
        document.querySelector('#category_table').style.display = 'none';
    }
})

if (document.querySelector('#category_table')) {

    categories_btn.addEventListener('click', function() {
        document.querySelector('#by_muscle_table').style.display = 'none';
        document.querySelector('#all_exc_table').style.display = 'none';   
    
        if (document.querySelector('#category_table')) {
            document.querySelector('#category_table').style.display = 'none';
        }
    })
}




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


// Adding a new exercise to workout program
const addExcBtn = document.querySelector("#addExcBtn");
const excDetailsBtn = document.querySelector('#excDetailsBtn');
const closeBtn = document.querySelector('#closeBtn');
const btnGroup = document.querySelector('#btnGroup')

addExcBtn.addEventListener('click', function() {
    document.querySelector('#btnGroup').style.display = 'none';
    document.querySelector('#addExcBtn').style.display = 'none';

    document.querySelector('#by_muscle_table').style.display = 'none';
    document.querySelector('#all_exc_table').style.display = 'none';

    if (document.querySelector('#category_table')) {
        document.querySelector('#category_table').style.display = 'none';
    }

    document.querySelector('#excDetails').style.display = 'block';
    document.querySelector('#excDetailsBtn').style.display = 'block';
})

closeBtn.addEventListener('click', function() {

    document.querySelector('#btnGroup').style.display = 'block';
    document.querySelector('#addExcBtn').style.display = 'block';
    document.querySelector('#by_muscle_table').style.display = 'none';
    document.querySelector('#all_exc_table').style.display = 'block';

    if (document.querySelector('#category_table')) {
        document.querySelector('#category_table').style.display = 'none';
    }

    document.querySelector('#excDetails').style.display = 'none';
    document.querySelector('#excDetailsBtn').style.display = 'none';
})



// Interaction for checkmark buttons during a w/o plan execution

const checkBtns = document.querySelectorAll('.checkBtn')

checkBtns.forEach(function(btn) {
    btn.addEventListener('click', function() {
        if (btn.style.backgroundColor !== 'green') {
            btn.style.backgroundColor = 'green';
            // btn.setAttribute('name', 'checkedBtn');
        } else {
            btn.style.backgroundColor = 'white';
            // btn.setAttribute('name', 'uncheckedBtn');
        }
    })
})