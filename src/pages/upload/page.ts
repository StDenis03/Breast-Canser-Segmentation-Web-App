import './style.css';

export default function (root: HTMLElement) {
  const section = document.createElement('div');
  section.innerHTML =  `
  <section id="center">
    <div>
      <h1>Hello, World!</h1>
      <p>Initial load</p>
    </div>
  </section>`;
  root.append(section);
}
