import style from './style.module.css';

export default function (root: HTMLElement) {
  const section = document.createElement('section');
  section.className = style.center;
  section.innerHTML =  `
    <div>
      <h1>Hello, World!</h1>
      <p>Initial load</p>
    </div>`;
  root.append(section);
}
