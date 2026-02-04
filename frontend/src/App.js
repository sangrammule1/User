import { useState } from "react";
import "./App.css";

function App() {
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    phone: ""
    });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    // For house_no, convert to integer if it's not empty, otherwise set to null
    const processedValue = name === "house_no" ? (value === "" ? null : parseInt(value, 10)) : value;
    
    setForm({ ...form, [name]: processedValue });
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors({ ...errors, [name]: "" });
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!form.first_name.trim()) {
      newErrors.first_name = "First name is required";
    }
    if (!form.last_name.trim()) {
      newErrors.last_name = "Last name is required";
    }
    if (!form.phone.trim()) {
      newErrors.phone = "Phone is required";
    }
    // No validation for email as it's nullable
    // No validation for house_no as it's nullable

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    try {
      const response = await fetch("http://localhost:6080/submit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(form)
      });

      const data = await response.json();
      alert(data.message);
      
      // Reset form on success
      if (response.ok) {
        setForm({
          first_name: "",
          last_name: "",
          phone: ""
        });
      }
    } catch (error) {
      alert("An error occurred. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="form-container">
      <div className="form-panel">
        <div className="form-header">
          <h2 className="form-title">Registration Form</h2>
          <p className="form-subtitle">Please fill in all required fields to complete your registration</p>
        </div>
        
        <form onSubmit={handleSubmit} className="registration-form">
          <div className="form-row">
            <div className="form-field">
              <label className="form-label">
                First Name<span className="required">*</span>
              </label>
              <div className="input-wrapper">
                <input
                  className={`form-input ${errors.first_name ? 'error' : ''}`}
                  name="first_name"
                  value={form.first_name}
                  onChange={handleChange}
                  placeholder="Enter first name"
                  required
                />
                <span className="input-icon">👤</span>
              </div>
              {errors.first_name && <span className="error-message">{errors.first_name}</span>}
            </div>

            <div className="form-field">
              <label className="form-label">
                Last Name<span className="required">*</span>
              </label>
              <div className="input-wrapper">
                <input
                  className={`form-input ${errors.last_name ? 'error' : ''}`}
                  name="last_name"
                  value={form.last_name}
                  onChange={handleChange}
                  placeholder="Enter last name"
                  required
                />
                <span className="input-icon">👤</span>
              </div>
              {errors.last_name && <span className="error-message">{errors.last_name}</span>}
            </div>
          </div>
          <div className="form-row">
            <div className="form-field">
              <label className="form-label">
                Phone<span className="required">*</span>
              </label>
              <div className="input-wrapper">
                <input
                  className={`form-input ${errors.phone ? 'error' : ''}`}
                  name="phone"
                  value={form.phone}
                  onChange={handleChange}
                  placeholder="Enter phone number"
                  required
                />
                <span className="input-icon">📞</span>
              </div>
              {errors.phone && <span className="error-message">{errors.phone}</span>}
            </div>
          </div>
          
          <div className="form-actions">
            <button type="button" className="cancel-button">
              <span>Cancel</span>
            </button>
            <button type="submit" className="submit-button" disabled={isSubmitting}>
              {isSubmitting ? (
                <>
                  <span className="spinner"></span>
                  <span>Submitting...</span>
                </>
              ) : (
                <>
                  <span>✓</span>
                  <span>Submit</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default App;