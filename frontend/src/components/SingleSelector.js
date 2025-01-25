import React, { useState } from "react";
import "../style/SingleSelector.css";

const SingleSelector = ({ title }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedValue, setSelectedValue] = useState("전체");
  const options = ["전체", "상주", "원격"];

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const selectOption = (value) => {
    setSelectedValue(value);
    setIsOpen(false);
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
