/** @format */

const main = document.querySelector('.main');
const accessToken =
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2OTA2NjMwNjB9.8FtClcRG_WebQGFpMtELj1wWEwVCHnqsmjJt4R2zhqM';
console.log('main', main);
async function getPost() {
  const response = await fetch(
    'https://python-fastapi-aac-6957907b7d1b.herokuapp.com/posts/',
    {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    }
  );
  const posts = await response.json();
  posts.forEach((post) => {
    const title = createDiv();
    title.textContent = post.Post.title;
    const content = createDiv();
    content.textContent = post.Post.content;

    main.appendChild(title);
    main.appendChild(content);
  });
}

function createDiv() {
  return document.createElement('DIV');
}

getPost();
