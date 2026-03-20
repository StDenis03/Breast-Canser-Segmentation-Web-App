import './page.css';

const appContainer = document.getElementById('app')!;

appContainer.innerHTML = `
<section id="center">
  <div>
    <h1>Hello, World!</h1>
    <p>Initial load</p>
  </div>
</section>
`;

document.body.append(appContainer);
