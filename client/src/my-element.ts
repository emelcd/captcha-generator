import { html, css, LitElement, CSSResultGroup } from "lit";
import { customElement, property } from "lit/decorators.js";

/**
 * An example element.
 *
 * @slot - This element has a slot
 * @csspart button - The button
 */
@customElement("my-element")
export class MyElement extends LitElement {
  static styles?: CSSResultGroup = css`
    :host {
      display: block;
    }
  `;

  @property({ type: String })
  captcha: string = "";

  @property({ type: String })
  uuid: string = "";

  @property({ type: String })
  value: string = "";

  async fetchCaptcha() {
    const response = await fetch("http://localhost:5000");
    const json = await response.json();
    const uuid = json.uuid;
    const img = await fetch(`http://localhost:5000/${uuid}`);
    const blob = await img.blob();
    const fileReader = new FileReader();
    fileReader.readAsDataURL(blob);
    fileReader.onload = () => {
      this.captcha = fileReader.result as string;
      this.uuid = uuid;
    };
  }

  connectedCallback(): void {
    super.connectedCallback();
    this.fetchCaptcha();
  }

  submitCaptcha(event: Event) {
    event.preventDefault();
    const body = {
      uuid: this.uuid,
      text: this.value,

    }
    fetch("http://localhost:5000", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(body)
    }).then(response => {
      return response.json();
    }).then(json => {
      const {result} = json
      if (result) {
        alert("Correct!")
      } else {
        alert("Incorrect!")
      }
    })
  }

  render() {
    return html`
      <section>
        <button @click="${this.fetchCaptcha}">Refresh</button>
        <div class="img-container">
          <img src="${this.captcha}" />
        </div>
        <div class="controllers-container">
          <form @submit=${this.submitCaptcha}>
            <input type="text" name="captcha" .value=${this.value} @change=${(e: Event) => (this.value = (e.target as HTMLInputElement).value)} />
            <button type="submit">Submit</button>

          </form>
        </div>
      </section>
    `;
  }
}

declare global {
  interface HTMLElementTagNameMap {
    "my-element": MyElement;
  }
}
