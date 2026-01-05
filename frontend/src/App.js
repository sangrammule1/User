import { useState } from "react";

function App() {
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    phone: "",
    email: ""
    });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch("http://localhost:8000/submit", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(form)
    });

    const data = await response.json();
    alert(data.message);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2 >Registration Form</h2 >

      <form onSubmit={handleSubmit}>
        <div >
          <label >First Name:</label > <br />
          <input
            name="first_name"
            value={form.first_name}
            onChange={handleChange}
            required
          />
        </div >

        <div >
          <label >Last Name:</label > <br />
          <input
            name="last_name"
            value={form.last_name}
            onChange={handleChange}
            required
          />
        </div >

        <div >
          <label >Phone:</label > <br />
          <input
            name="phone"
            value={form.phone}
            onChange={handleChange}
            required
          />
        </div>
        
        <div >
          <label >Email:</label > <br />
          <input
            name="email"
            value={form.email}
            onChange={handleChange}
            required
          />
        </div>
        <br/>
        <button type="submit">Submit</button>
      </form>
    </div >
  );
}

export default App;