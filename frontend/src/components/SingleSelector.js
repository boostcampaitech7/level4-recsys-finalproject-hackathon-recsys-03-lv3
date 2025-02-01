import React, { useState } from "react";
import "../style/Selectors.css";

const SingleSelector = ({ title, options, onChange }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedValue, setSelectedValue] = useState(options[0]);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const selectOption = (value) => {
    setSelectedValue(value);
    setIsOpen(false);
    onChange(value);
  };

  return (
    <div className="single-selector">
      <div className="label-container" onClick={toggleDropdown}>
        <span className="label">{title}</span>
        <span className="selected-value">{selectedValue}</span>
        <span className={`arrow ${isOpen ? "open" : ""}`}>
          <i className="bi bi-caret-down-fill"></i>
        </span>
      </div>
      {isOpen && (
        <div className="dropdown-menu">
          <ul className="dropdown-list">
            {options.map((option) => (
              <li
                key={option}
                className={`dropdown-item ${
                  option === selectedValue ? "selected" : ""
                }`}
                onClick={() => selectOption(option)}
              >
                {option === selectedValue && (
                  <span className="checkmark">
                    <i className="bi bi-check"></i>
                  </span>
                )}
                {option}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default SingleSelector;
