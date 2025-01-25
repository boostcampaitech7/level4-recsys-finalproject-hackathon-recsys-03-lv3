import React, { useState } from "react";
import "../style/Selectors.css";

const MultiSelector = ({ title }) => {
  const [isOpen, setIsOpen] = useState(false); // 드롭다운 상태
  const [selectedCategory, setSelectedCategory] = useState(""); // 선택한 직군
  const [selectedRoles, setSelectedRoles] = useState([]); // 선택한 직무

  // 실제 데이터 (DB에서 가져올 데이터)
  const categories = {
    개발: [
      "백엔드 개발자",
      "프론트엔드 개발자",
      "풀스택 개발자",
      "데이터 엔지니어",
      "머신러닝 엔지니어",
    ],
  };

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const handleCategorySelect = (category) => {
    setSelectedCategory(category);
    setSelectedRoles([]); // 직군 변경 시 직무 초기화
  };

  const handleRoleSelect = (role) => {
    const allRoles = categories[selectedCategory];

    if (role === "전체") {
      if (selectedRoles.length === allRoles.length) {
        setSelectedRoles([]); // 전체 해제
      } else {
        setSelectedRoles([...allRoles]); // 전체 선택
      }
    } else {
      const updatedRoles = selectedRoles.includes(role)
        ? selectedRoles.filter((r) => r !== role) // 선택 해제
        : [...selectedRoles, role]; // 선택 추가

      setSelectedRoles(updatedRoles);
    }
  };

  const isAllSelected = () => {
    const allRoles = categories[selectedCategory];
    return selectedRoles.length === allRoles.length;
  };

  return (
    <div className="multi-selector">
      {/* 선택된 값과 화살표 */}
      <div className="label-container" onClick={toggleDropdown}>
        <span className="label">{title}</span>
        <span className="selected-value">
          {selectedCategory
            ? `${selectedCategory} | ${
                isAllSelected() ? "전체 선택" : `${selectedRoles.length}개 선택`
              }`
            : "선택하세요"}
        </span>
        <span className={`arrow ${isOpen ? "open" : ""}`}>
          <i className="bi bi-caret-down-fill"></i>
        </span>
      </div>

      {isOpen && (
        <div className="dropdown-menu">
          {/* 직군 선택 */}
          {!selectedCategory && (
            <ul className="dropdown-list">
              {Object.keys(categories).map((category) => (
                <li
                  key={category}
                  className="dropdown-item"
                  onClick={() => handleCategorySelect(category)}
                >
                  {category}
                </li>
              ))}
            </ul>
          )}

          {/* 직무 선택 */}
          {selectedCategory && (
            <ul className="dropdown-list scrollable">
              {/* 가상의 "전체" 옵션 추가 */}
              <li
                key="전체"
                className="dropdown-item 전체-option"
                onClick={() => handleRoleSelect("전체")}
              >
                {isAllSelected() ? (
                  <span className="checkmark">
                    <i className="bi bi-check"></i>
                  </span>
                ) : null}
                전체
              </li>
              <li className="divider"></li>
              {categories[selectedCategory].map((role) => (
                <li
                  key={role}
                  className={`dropdown-item ${
                    selectedRoles.includes(role) ? "selected" : ""
                  }`}
                  onClick={() => handleRoleSelect(role)}
                >
                  {selectedRoles.includes(role) && (
                    <span className="checkmark">
                      <i className="bi bi-check"></i>
                    </span>
                  )}
                  {role}
                </li>
              ))}
              {/* '뒤로 가기' 옵션 */}
              <li
                className="dropdown-item back-option"
                onClick={() => setSelectedCategory("")}
              >
                <i className="bi bi-arrow-left"></i>뒤로
              </li>
            </ul>
          )}
        </div>
      )}
    </div>
  );
};

export default MultiSelector;
