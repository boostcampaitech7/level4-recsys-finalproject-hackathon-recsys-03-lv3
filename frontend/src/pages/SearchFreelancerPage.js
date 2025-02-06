import React, { useState } from "react";
import FreelancerInfo from "../components/FreelancerInfo";
import MultiSelector from "../components/MultiSelector";
import SingleSelector from "../components/SingleSelector";
import "../style/SearchPages.css";
import profile1 from "../assets/profile_example1.jpg";
import profile2 from "../assets/profile_example2.jpg";
import profile3 from "../assets/profile_example3.jpg";

const SearchFreelancer = () => {
  const freelancers = [
    {
      photo: profile1,
      freelancerId: 122,
      freelancerName: "희수희수야",
      workExp: "7년",
      workType: "원격",
      role: "백엔드 개발자",
      freelancerContent:
        "27년 차 Java 개발자로, 백엔드와 프론트엔드 개발에 모두 능숙합니다. 데이터베이스 설계 및 관리 경험이 풍부하며, 앱 개발과 배포까지 전 과정을 주도한 경험이 있습니다.",
      locationName: "양산",
      categoryList: ["IT•정보통신업", "건설업"],
      skillList: [
        { skillName: "Java", skillScore: 4.5 },
        { skillName: "Spring Boot", skillScore: 4 },
        { skillName: "jQuery", skillScore: 3.5 },
        { skillName: "SQL", skillScore: 4.5 },
        { skillName: "AJAX", skillScore: 3 },
        { skillName: "JSP", skillScore: 4 },
      ],
      feedbackCount: 12,
      expertise: 4.2,
      proactiveness: 4.3,
      punctuality: 4.1,
      maintainability: 4.0,
      communication: 4.4,
    },
    {
      photo: profile2,
      freelancerId: 123,
      freelancerName: "박왕균이",
      workExp: "3년",
      workType: "원격",
      role: "프론트엔드 개발자",
      freelancerContent:
        "웹 애플리케이션 개발, 클라우드 관리 시스템 개발, 모바일 앱 개발, 금융 백엔드 시스템 개발, 게임 클라이언트/서버 개발 등 다양한 업무의 개발 경험이 있으며, 서비스 운영 경험을 다년간 지니고 있는 시니어 개발자.",
      locationName: "서울",
      categoryList: ["제조업", "IT•정보통신업"],
      skillList: [
        { skillName: "Python", skillScore: 5 },
        { skillName: "PyTorch", skillScore: 4 },
        { skillName: "Tensorflow", skillScore: 4.5 },
        { skillName: "HTML", skillScore: 2 },
        { skillName: "Vue.js", skillScore: 4 },
        { skillName: "CSS", skillScore: 3.5 },
      ],
      feedbackCount: 18,
      expertise: 4.7,
      proactiveness: 4.8,
      punctuality: 4.6,
      maintainability: 4.5,
      communication: 4.7,
    },
    {
      photo: profile3,
      freelancerId: 124,
      freelancerName: "성택의선택",
      workExp: "5년",
      workType: "대면",
      role: "백엔드 개발자",
      freelancerContent:
        "혁신적인 것을 더 많이 만들 수 있는 다재다능한 능력을 가진 경험이 풍부한 베테랑 개발자입니다. 보다 효율적이고 신속적인 접근으로 문제 해결을 중심으로 역할을 수행하고 있습니다.",
      locationName: "서울",
      categoryList: ["제조업", "IT•정보통신업"],
      skillList: [
        { skillName: "Java", skillScore: 4 },
        { skillName: "Spring Boot", skillScore: 4.5 },
        { skillName: "jQuery", skillScore: 3.5 },
        { skillName: "SQL", skillScore: 4 },
        { skillName: "AJAX", skillScore: 3 },
        { skillName: "JSP", skillScore: 1 },
      ],
      feedbackCount: 18,
      expertise: 4.7,
      proactiveness: 4.8,
      punctuality: 4.6,
      maintainability: 4.5,
      communication: 4.7,
    },
  ];

  freelancers.forEach((freelancer) => {
    const {
      expertise,
      proactiveness,
      punctuality,
      maintainability,
      communication,
    } = freelancer;
    freelancer.feedbackScore =
      (expertise +
        proactiveness +
        punctuality +
        maintainability +
        communication) /
      5;
  });

  const skillList = [
    "Bash/Shell (all shells)",
    "Go",
    "HTML/CSS",
    "Java",
    "JavaScript",
    "Python",
    "TypeScript",
    "Dynamodb",
    "MongoDB",
    "PostgreSQL",
    "Amazon Web Services (AWS)",
    "Heroku",
    "Netlify",
    "Express",
    "Next.js",
    "Node.js",
    "React",
    "Docker",
    "Homebrew",
    "Kubernetes",
    "npm",
    "Vite",
    "Webpack",
    "C#",
    "Firebase Realtime Database",
    "Google Cloud",
    "ASP.NET CORE",
    ".NET (5+) ",
    ".NET Framework (1.0 - 4.8)",
    ".NET MAUI",
    "MSBuild",
    "MySQL",
    "Redis",
    "Digital Ocean",
    "Firebase",
    "Vercel",
    "C",
    "C++",
    "Delphi",
    "PowerShell",
    "SQL",
    "VBA",
    "Visual Basic (.Net)",
    "Microsoft Access",
    "Microsoft SQL Server",
    "SQLite",
    "Cloudflare",
    "ASP.NET",
    "jQuery",
    "RabbitMQ",
    "Xamarin",
    "Yarn",
    "Hetzner",
    "VMware",
    "Ansible",
    "Chocolatey",
    "Make",
    "NuGet",
    "Pacman",
    "Pip",
    "Terraform",
    "Oracle",
    "Blazor",
    "Roslyn",
    "React Native",
    "PHP",
    "Microsoft Azure",
    "MariaDB",
    "Apache Kafka",
    "Godot",
    "Maven (build tool)",
    "F#",
    "Django",
    "WordPress",
    "Pandas",
    "Clojure",
    "Snowflake",
    "Cordova",
    "DirectX",
    "OpenCL",
    "Opencv",
    "Visual Studio Solution",
    "Scala",
    "Presto",
    "Apache Spark",
    "Lua",
    "Nix",
    "AngularJS",
    "Perl",
    "Angular",
    "Flask",
    "Keras",
    "NumPy",
    "Scikit-Learn",
    "TensorFlow",
    "Databricks SQL",
    "DuckDB",
    "Databricks",
    "Elasticsearch",
    "CodeIgniter",
    "NestJS",
    "Cassandra",
    "FastAPI",
    "Ruff",
    "OCaml",
    "H2",
    "Oracle Cloud Infrastructure (OCI)",
    "Spring Boot",
    "Spring Framework",
    "Torch/PyTorch",
    "Gradle",
    "Neo4J",
    "PythonAnywhere",
    "CUDA",
    "Hugging Face Transformers",
    "mlflow",
    "Ruby",
    "Ruby on Rails",
    "Vue.js",
    "pnpm",
    "Fly.io",
    "Render",
    "OpenGL",
    "Rust",
    "Fastify",
    "Tauri",
    "Bun",
    "Assembly",
    "MATLAB",
    "Unity 3D",
    "Unreal Engine",
    "Cosmos DB",
    "Dart",
    "Fortran",
    "Julia",
    "BigQuery",
    "Qt",
    "Ninja",
    "Crystal",
    "R",
    "Tidyverse",
    "Firebird",
    "Clickhouse",
    "Cloud Firestore",
    "Supabase",
    "Solid.js",
    "Electron",
    "Kotlin",
    "Managed Hosting",
    "Laravel",
    "OpenShift",
    "Flutter",
    "Haskell",
    "Hadoop",
    "Ada",
    "Elixir",
    "Erlang",
    "Groovy",
    "Lisp",
    "Zig",
    "InfluxDB",
    "Deno",
    "Htmx",
    "Phoenix",
    "Remix",
    "Svelte",
    "Capacitor",
    "Ionic",
    "Composer",
    "APT",
    "Google Test",
    "Quarkus",
    "Ant",
    "GDScript",
    "Symfony",
    "SwiftUI",
    "IBM DB2",
    "Drupal",
    "OVH",
    "Elm",
    "Gatsby",
    "Nuxt.js",
    "Objective-C",
    "Swift",
    "Strapi",
    "Yii 2",
    "GTK",
    "Podman",
    "Astro",
    "Ktor",
    "Dagger",
    "Prolog",
    "Solr",
    "MFC",
    "Vultr",
    "EventStoreDB",
    "RavenDB",
    "Couch DB",
    "JAX",
    "Cockroachdb",
    "IBM Cloud Or Watson",
    "Pulumi",
    "Couchbase",
    "Cobol",
    "Puppet",
    "Linode, now Akamai",
    "Scaleway",
    "Play Framework",
    "Nim",
    "Apex",
    "OpenStack",
    "Solidity",
    "Colocation",
    "MicroPython",
    "Chef",
    "Alibaba Cloud",
    "Zephyr",
    "TiDB",
    "Datomic",
  ];

  const roleList = ["백엔드 개발자", "프론트엔드 개발자"];

  const [filterRoles, setFilterRoles] = useState(roleList);
  const [filterWorkType, setFilterWorkType] = useState("근무 형태");
  const [filterSkillList, setFilterSkillList] = useState(skillList);
  const [sortOption, setSortOption] = useState("최신순");

  // 필터링 로직
  const filteredFreelancers = freelancers
    .filter((freelancer) => {
      return (
        filterRoles.includes(freelancer.role) &&
        (filterWorkType === "근무 형태" ||
          freelancer.workType === filterWorkType) &&
        freelancer.skillList.some((skill) =>
          filterSkillList.includes(skill.skillName)
        )
      );
    })
    .sort((a, b) => {
      // 정렬 로직
      if (sortOption === "최신순") return b.freelancerId - a.freelancerId;
      if (sortOption === "매칭 점수 높은순")
        return b.matchingScore - a.matchingScore;
      return 0;
    });

  const resetFilters = () => {
    setFilterRoles(roleList);
    setFilterWorkType("근무 형태");
    setFilterSkillList(skillList);
    setSortOption("최신순");
  };

  return (
    <div className="search-freelancer-container">
      <div className="header-container">
        <h3 className="header">프리랜서 리스트</h3>
        <p>총 {freelancers.length}명의 프리랜서가 있습니다.</p>
      </div>
      <div className="filters">
        <div className="filter-group-left">
          {/* 직군 필터 */}
          <MultiSelector
            title="직군/직무"
            options={roleList}
            onChange={setFilterRoles}
            value={filterRoles}
          />

          {/* 근무 형태 필터 */}
          <SingleSelector
            title="근무 형태"
            options={["근무 형태", "원격", "대면"]}
            onChange={setFilterWorkType}
            value={filterWorkType}
          />

          {/* 스킬 필터 */}
          <MultiSelector
            title="스킬"
            options={skillList}
            onChange={setFilterSkillList}
            value={filterSkillList}
          />

          {/* 필터 초기화 버튼 */}
          <button className="reset-button" onClick={resetFilters}>
            <i className="bi bi-arrow-counterclockwise"></i> 필터 초기화
          </button>
        </div>

        {/* 정렬 옵션 */}
        <div className="filter-group-right">
          <SingleSelector
            title="정렬 기준"
            options={["최신순"]}
            onChange={setSortOption}
            value={sortOption}
          />
        </div>
      </div>
      {filteredFreelancers.map((freelancer) => (
        <FreelancerInfo
          key={freelancer.freelancerId}
          freelancerInfo={freelancer}
          pageType="search"
        />
      ))}
    </div>
  );
};

export default SearchFreelancer;
