import React, { useState } from "react";
import "../style/Selectors.css";

const MultiSelector = ({ title, options, onChange }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedValues, setSelectedValues] = useState(options);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const toggleOption = (value) => {
    let updatedValues = [...options];

    if (value === "전체") {
      if (selectedValues.length === options.length) {
        updatedValues = [];
      } else {
        updatedValues = [...options];
      }
    } else if (selectedValues.includes(value)) {
      // 이미 선택된 값이면 제거
      updatedValues = selectedValues.filter((item) => item !== value);
    } else {
      // 선택되지 않은 값이면 추가
      updatedValues = [...selectedValues, value];
    }
    setSelectedValues(updatedValues);
    onChange(updatedValues); // 선택된 값 리스트 업데이트
  };

  return (
    <div className="multi-selector">
      <div className="label-container" onClick={toggleDropdown}>
        {/* <span className="label">{title}</span> */}
        <span className="selected-value">
          {selectedValues.length === options.length
            ? title
            : selectedValues.length > 0
              ? selectedValues.join(", ")
              : "선택 없음"}
        </span>
        <span className={`arrow ${isOpen ? "open" : ""}`}>
          <i className="bi bi-caret-down-fill"></i>
        </span>
      </div>
      {isOpen && (
        <div className="dropdown-menu">
          <ul className="dropdown-list">
            <li
              key="전체"
              className="dropdown-item 전체-option"
              onClick={() => toggleOption("전체")}
            >
              {selectedValues.length === options.length ? (
                <span className="checkmark">
                  <i className="bi bi-check"></i>
                </span>
              ) : null}
              전체
            </li>
            <li className="divider"></li>
            {options.map((option) => (
              <li
                key={option}
                className={`dropdown-item ${
                  selectedValues.includes(option) ? "selected" : ""
                }`}
                onClick={() => toggleOption(option)}
              >
                {selectedValues.includes(option) && (
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

export default MultiSelector;
