document.addEventListener("DOMContentLoaded", function () {
    const blogsContainer = document.getElementById("blogs-container");
    const blogForm = document.getElementById("blog-form");

    function fetchBlogs() {
        axios.get("http://127.0.0.1:8000/blogs/")
            .then(response => {
                const blogs = response.data;
                blogsContainer.innerHTML = "";

                for (const blogId in blogs) {
                    const blog = blogs[blogId];
                    const blogElement = document.createElement("div");
                    blogElement.innerHTML = `<strong>${blog.title}</strong>: ${blog.content} <button onclick="deleteBlog(${blogId})">Delete</button>`;
                    blogsContainer.appendChild(blogElement);
                }
            })
            .catch(error => console.error(error));
    }

    function createBlog(title, content) {
        axios.post("http://127.0.0.1:8000/blogs/", {
            title: title,
            content: content
        })
        .then(response => {
            console.log("Blog created:", response.data);
            fetchBlogs(); 
        })
        .catch(error => console.error(error));
    }

    function deleteBlog(blogId) {
        axios.delete(`http://127.0.0.1:8000/blogs/${blogId}`)
        .then(response => {
            console.log("Blog deleted:", response.data);
            fetchBlogs(); 
        })
        .catch(error => console.error(error));
    }

    blogForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const title = document.getElementById("title").value;
        const content = document.getElementById("content").value;
        createBlog(title, content);
    });

    // Initial fetch of blogs when the page loads
    fetchBlogs();
});
