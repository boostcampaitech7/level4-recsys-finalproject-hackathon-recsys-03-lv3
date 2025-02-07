import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import logo from "../assets/logo_primary.png";
import SingleSelector from "../components/SingleSelector";
import MultiSelector from "../components/MultiSelector";
import "../style/SignUpPage.css";

const SignUpFreelancer = () => {
  const navigate = useNavigate();

  const [locationOptions, setLocationOptions] = useState([]);
  const [locationIdMap, setLocationIdMap] = useState();
  const [selectedLocation, setSelectedLocation] = useState("거주 지역");

  const [categoryOptions, setCategoryOptions] = useState([]);
  const [categoryIdMap, setCategoryIdMap] = useState();
  const [skillOptions, setSkillOptions] = useState([]);
  const [skillIdMap, setSkillIdMap] = useState();

  const [selectedWorkType, setSelectedWorkType] = useState("근무 형태");
  const [selectedRole, setSelectedRole] = useState("직무");

  // API에서 받아온 데이터 불러오기
  useEffect(() => {
    const loadData = async () => {
      const locationList = JSON.parse(
        sessionStorage.getItem("location") || "[]"
      );
      const categoryList = JSON.parse(
        sessionStorage.getItem("category") || "[]"
      );
      const skillList = JSON.parse(sessionStorage.getItem("skill") || "[]");

      if (locationList.length > 0) {
        setLocationOptions(
          locationList.map((loc) => loc?.locationName || "알 수 없음")
        );
        setLocationIdMap(
          locationList.reduce((acc, loc) => {
            acc[loc?.locationName] = loc?.locationId;
            return acc;
          }, {})
        );
      }

      // 전문 분야(카테고리) 옵션 설정
      if (categoryList.length > 0) {
        setCategoryOptions(
          categoryList.map((cat) => cat?.categoryName || "알 수 없음")
        );
        setCategoryIdMap(
          categoryList.reduce((acc, cat) => {
            acc[cat?.categoryName] = cat?.categoryId;
            return acc;
          }, {})
        );
      }

      // 보유 스킬 옵션 설정
      if (skillList.length > 0) {
        setSkillOptions(
          skillList.map((skill) => skill?.skillName || "알 수 없음")
        );
        setSkillIdMap(
          skillList.reduce((acc, skill) => {
            acc[skill?.skillName] = skill?.skillId;
            return acc;
          }, {})
        );
      }
    };

    loadData();
  }, []);

  // 근무 형태
  const workTypeOptions = ["대면", "원격", "상관 없음"];
  const workTypeIdMap = { 대면: 0, 원격: 1, "상관 없음": 2 };

  // 직무 리스트
  const roleOptions = [
    "풀스택 개발자",
    "백엔드 개발자",
    "프론트엔드 개발자",
    "모바일 개발자",
    "임베디드 개발자",
    "데스크톱/엔터프라이즈 개발자",
    "QA/테스트 개발자",
    "AI 개발자",
    "게임/그래픽 개발자",
    "데이터 엔지니어",
    "데이터 분석가",
    "데이터 사이언티스트/ML 전문가",
    "클라우드 엔지니어",
    "DevOps 엔지니어",
    "디자이너",
    "블록체인 엔지니어",
    "DB 관리자",
  ];

  const [error, setError] = useState(null);

  // 입력 필드 상태 관리
  const [formData, setFormData] = useState({
    freelancerName: "",
    email: "",
    password: "",
    confirmPassword: "",
    workExp: "",
    price: "",
    workType: null,
    role: null,
    freelancerContent: "",
    locationId: null,
    categoryList: [],
    skillList: [],
  });

  // 가격 입력 포맷팅 (천 단위 콤마)
  const formatPrice = (value) => {
    const numericValue = value.replace(/[^0-9]/g, "");
    return numericValue.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  };

  const handlePriceChange = (e) => {
    setFormData({ ...formData, price: formatPrice(e.target.value) });
  };

  // 입력 필드 값 변경 핸들러
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // 회원가입 요청
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    console.log(formData);
    const headers = {
      Accept: "application/json",
    };
    if (formData.password !== formData.confirmPassword) {
      setError("비밀번호가 일치하지 않습니다.");
      return;
    }

    try {
      const response = await axios.post(
        `${process.env.REACT_APP_BASE_URL}/api/auth/register/freelancer`,
        {
          freelancerName: formData.freelancerName,
          email: formData.email,
          password: formData.password,
          workExp: formData.workExp,
          price: parseInt(formData.price.replace(/,/g, "")),
          workType: workTypeIdMap[formData.workType] ?? null,
          role: formData.role ?? null,
          freelancerContent: formData.freelancerContent,
          locationId: locationIdMap[formData.locationId] ?? null,
          categoryList: formData.categoryList.map((cat) => categoryIdMap[cat]),
          skillList: formData.skillList.map((skill) => skillIdMap[skill]),
        },
        { headers }
      );

      if (response.status === 200) {
        alert("회원가입이 완료되었습니다.");
        navigate("/login");
      }
    } catch (err) {
      setError(err.response?.data?.message || "회원가입에 실패했습니다.");
    }
  };

  return (
    <div id="signup-freelancer-page" className="signup-container">
      <div className="signup-card">
        <div className="signup-logo">
          <img src={logo} alt="Harmony Logo" />
        </div>
        <p className="signup-header">
          프리랜서로 가입 후, 당신과 잘 맞는 프로젝트를 만나보아요!
        </p>

        {error && <p className="error-message">{error}</p>}

        <form onSubmit={handleSubmit} className="signup-form">
          <div className="form-grid">
            {/* 입력 필드 (왼쪽) */}
            <div className="form-left">
              <input
                type="text"
                name="freelancerName"
                placeholder="이름"
                value={formData.freelancerName}
                onChange={handleChange}
                required
              />
              <input
                type="email"
                name="email"
                placeholder="이메일"
                value={formData.email}
                onChange={handleChange}
                required
              />
              <input
                type="password"
                name="password"
                placeholder="비밀번호"
                value={formData.password}
                onChange={handleChange}
                required
              />
              <input
                type="password"
                name="confirmPassword"
                placeholder="비밀번호 확인"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
              />
              <input
                type="text"
                name="workExp"
                placeholder="경력 (년)"
                value={formData.workExp}
                onChange={handleChange}
                required
              />
              <input
                type="text"
                name="price"
                placeholder="연봉 (원)"
                value={formData.price}
                onChange={handlePriceChange}
                required
              />
            </div>

            {/* 셀렉터 (오른쪽) */}
            <div className="form-right">
              <SingleSelector
                options={locationOptions}
                value={selectedLocation}
                onChange={setSelectedLocation}
              />
              <SingleSelector
                options={workTypeOptions}
                value={selectedWorkType}
                onChange={setSelectedWorkType}
              />
              <SingleSelector
                options={roleOptions}
                value={selectedRole}
                onChange={setSelectedRole}
              />
              <MultiSelector
                title="전문 분야"
                options={categoryOptions}
                value={formData.categoryList}
                onChange={(selected) =>
                  setFormData({ ...formData, categoryList: selected })
                }
              />
              <MultiSelector
                title="보유 스킬"
                options={skillOptions}
                value={formData.skillList}
                onChange={(selected) =>
                  setFormData({ ...formData, skillList: selected })
                }
              />
            </div>
          </div>

          <button type="submit" className="signup-button">
            회원가입 완료
          </button>
        </form>
      </div>
    </div>
  );
};

export default SignUpFreelancer;
