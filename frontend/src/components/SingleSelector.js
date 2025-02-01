import React, { useState, useEffect } from "react";
import "../style/Selectors.css";

const SingleSelector = ({ title, options, value, onChange }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedValue, setSelectedValue] = useState(value || options[0]);

  // 외부에서 value가 변경되면 내부 상태를 업데이트
  useEffect(() => {
    if (value !== undefined) {
      setSelectedValue(value);
    }
  }, [value]);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const selectOption = (option) => {
    setSelectedValue(option);
    setIsOpen(false);
    onChange(option);
  };

  return (
    <div className="single-selector">
      <div className="label-container" onClick={toggleDropdown}>
        <span className="label visually-hidden">{title}</span>
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
