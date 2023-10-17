
document.addEventListener('DOMContentLoaded', function() {
    var contentContainer = document.querySelector('.contentcontainer');
    var ele='a';
    acms=JSON.parse(acms);
    users=JSON.parse(users);
    function createContentDiv() {
        var content = document.createElement('div');
        content.className = 'content'; // Set the class to "content"
        return content;
    }

    function showAcms() {
        ele='a';
        contentContainer.innerHTML = '';
        var content = document.createElement('div');
        content.className = 'contenttitle';
        content.innerHTML = `<p>Email Id</p><p>Name</p><p>Contact No</p>`;
        contentContainer.appendChild(content);
        acms.forEach(function(acm) {
            var content = createContentDiv();
            content.innerHTML = `<p>${acm.acmid}</p><p>${acm.name}</p><p>${acm.phno}</p>`;
            contentContainer.appendChild(content);
        });
    }

    // Function to display Users content
    function showUsers() {
        ele='u';
        contentContainer.innerHTML = '';
        
        var content = document.createElement('div');
        content.className = 'contenttitle';
        content.innerHTML = `<p>Email Id</p><p>Name</p><p>Contact No</p>`;
        contentContainer.appendChild(content);
        users.forEach(function(user) {
            var content = createContentDiv();
            content.innerHTML = `<p>${user.mailid}</p><p>${user.name}</p><p>${user.phno}</p>`;
            contentContainer.appendChild(content);
        });
    }

    // Attach click event handlers to the buttons
    document.getElementById('acmsButton').addEventListener('click', showAcms);
    document.getElementById('usersButton').addEventListener('click', showUsers);
    showAcms();


    var searchbar=document.getElementById("searchid");
    searchbar.addEventListener("input",function(){
        var data = (ele === 'a') ? acms : users;
        contentContainer.innerHTML = '';
        data.forEach(function (item) {
            if (item.acmid.toLowerCase().includes(searchText) || item.name.toLowerCase().includes(searchText) || item.phno.toLowerCase().includes(searchText)) {
                var content = createContentDiv();
                content.innerHTML = `<p>${item.acmid}</p><p>${item.name}</p><p>${item.phno}</p>`;
                contentContainer.appendChild(content);
            }
        });
        })

});
