document.addEventListener('DOMContentLoaded', function() {
    var filterIcon = document.querySelector('.filtericon');
    var filter = document.querySelector('.filter');
    
    filterIcon.addEventListener('click', function() {
        if (filter.style.opacity === '0') {
            filter.style.opacity = '1';
        } else {
            filter.style.opacity = '0';
        }
    });
});
