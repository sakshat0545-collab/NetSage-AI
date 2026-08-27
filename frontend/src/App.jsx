import { useState } from "react";
import axios from "axios";

import {
  Activity,
  AlertTriangle,
  BrainCircuit,
  CheckCircle2,
  ChevronRight,
  Clock3,
  FileSearch,
  History,
  LayoutDashboard,
  Network,
  Settings,
  ShieldCheck,
  Terminal,
  UserCheck,
  XCircle,
  RefreshCw,
} from "lucide-react";

// =========================================================
// NETSAGE AI
// FRONTEND APPLICATION
// =========================================================

function App() {
  // =====================================================
  // FORM STATE
  // =====================================================

  const [symptom, setSymptom] = useState("");
  const [topology, setTopology] = useState("");
  const [showOutput, setShowOutput] = useState("");

  // =====================================================
  // APPLICATION STATE
  // =====================================================

  const [diagnosis, setDiagnosis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [reviewStatus, setReviewStatus] = useState("pending");
  const [reviewLoading, setReviewLoading] = useState(false);
  const [reviewError, setReviewError] = useState("");
  const [showEditReview, setShowEditReview] = useState(false);
  const [reviewerNote, setReviewerNote] = useState("");
  const [editedIssue, setEditedIssue] = useState("");
  const [editedRootCause, setEditedRootCause] = useState("");
  const [editedAction, setEditedAction] = useState("");

  // =====================================================
  // ANALYZE NETWORK
  // =====================================================

  const handleAnalyze = async () => {
    if (!symptom.trim()) {
      setError("Please describe the network symptom.");
      return;
    }

    if (!topology.trim()) {
      setError("Please provide the network topology.");
      return;
    }

    if (!showOutput.trim()) {
      setError("Please provide Cisco command evidence.");
      return;
    }

    setLoading(true);
    setError("");
    setDiagnosis(null);
    setReviewStatus("pending");

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/diagnose",
        {
          symptom: symptom,
          topology: topology,
          show_output: showOutput,
        }
      );

      console.log("NetSage AI Response:", response.data);
      setDiagnosis(response.data);
    } catch (err) {
      console.error("Diagnosis request failed:", err);

      if (err.response) {
        setError(
          `Backend error ${err.response.status}: ` +
            (err.response.data?.detail || "The backend rejected the request.")
        );
      } else {
        setError(
          "Unable to connect to NetSage AI backend. " +
            "Make sure the FastAPI server is running."
        );
      }
    } finally {
      setLoading(false);
    }
  };

  // =====================================================
  // CLEAR CASE
  // =====================================================

  const handleReset = () => {
    setSymptom("");
    setTopology("");
    setShowOutput("");
    setDiagnosis(null);
    setError("");
    setReviewStatus("pending");
    setReviewLoading(false);
    setReviewError("");
    setShowEditReview(false);
    setReviewerNote("");
    setEditedIssue("");
    setEditedRootCause("");
    setEditedAction("");
  };

  // =====================================================
  // HUMAN REVIEW
  // =====================================================

  const submitReview = async (
    decision,
    customIssue = null,
    customRootCause = null,
    customAction = null
  ) => {
    if (!diagnosis) {
      setReviewError("Run a diagnosis before submitting a human review.");
      return;
    }

    setReviewLoading(true);
    setReviewError("");

    const caseId =
      diagnosis?.case?.case_id ||
      diagnosis?.case?.id ||
      diagnosis?.case_id ||
      `CASE-${Date.now()}`;

    const payload = {
      case_id: caseId,
      ai_issue: issueType,
      ai_root_cause: rootCause,
      ai_action: recommendedAction,
      human_decision: decision.toUpperCase(),
      human_issue: customIssue,
      human_root_cause: customRootCause,
      human_action: customAction,
      reviewer_note: reviewerNote,
    };

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/review",
        payload
      );

      console.log("NetSage human review response:", response.data);
      setReviewStatus(decision.toLowerCase());

      if (decision === "EDIT") {
        setShowEditReview(false);
      }
    } catch (err) {
      console.error("Human review request failed:", err);

      if (err.response) {
        setReviewError(
          `Review error ${err.response.status}: ` +
            (err.response.data?.detail || "The backend rejected the review.")
        );
      } else {
        setReviewError("Unable to connect to the NetSage AI review service.");
      }
    } finally {
      setReviewLoading(false);
    }
  };

  const handleReview = async (status) => {
    if (status === "edited") {
      setEditedIssue(issueType);
      setEditedRootCause(rootCause);
      setEditedAction(recommendedAction);
      setShowEditReview(true);
      setReviewError("");
      return;
    }

    await submitReview(status === "accepted" ? "ACCEPT" : "REJECT");
  };

  const handleSubmitEditedReview = async () => {
    await submitReview(
      "EDIT",
      editedIssue.trim() || issueType,
      editedRootCause.trim() || rootCause,
      editedAction.trim() || recommendedAction
    );
  };

  // =====================================================
  // BACKEND RESPONSE NORMALIZATION
  // =====================================================

  const ruleChecker = diagnosis?.rule_checker || {};
  const intelligence = diagnosis?.cisco_intelligence || {};
  const parsedEvidence = diagnosis?.parsed_evidence || {};

  // Rule Results
  const ruleResults = Array.isArray(ruleChecker?.results)
    ? ruleChecker.results
    : [];

  const primaryIssue =
    ruleResults.find((result) => result?.status === "ISSUE") || null;

  const firstPassedCheck =
    ruleResults.find((result) => result?.status === "PASS") || null;

  // Issue Type
  const issueType =
    intelligence?.issue_type ||
    diagnosis?.issue_type ||
    primaryIssue?.check ||
    "No issue classified";

  // Root Cause
  const rootCause =
    intelligence?.root_cause ||
    diagnosis?.root_cause ||
    primaryIssue?.details ||
    (primaryIssue
      ? `${primaryIssue.check} issue detected`
      : "Awaiting network analysis");

  // Confidence
  const confidence =
    intelligence?.confidence ||
    diagnosis?.confidence ||
    (primaryIssue ? "High" : diagnosis ? "Medium" : "—");

  // Technical Reason
  const technicalReason =
    intelligence?.technical_reason ||
    diagnosis?.technical_reason ||
    primaryIssue?.details ||
    (firstPassedCheck?.details || "No technical reasoning available yet.");

  // Evidence
  let evidence = [];
  if (Array.isArray(intelligence?.evidence)) {
    evidence = intelligence.evidence;
  } else if (Array.isArray(diagnosis?.evidence)) {
    evidence = diagnosis.evidence;
  } else if (primaryIssue?.evidence && Array.isArray(primaryIssue.evidence)) {
    evidence = primaryIssue.evidence;
  } else if (parsedEvidence && Object.keys(parsedEvidence).length > 0) {
    const evidenceItems = [];
    if (Array.isArray(parsedEvidence.host_ips)) {
      evidenceItems.push(...parsedEvidence.host_ips.map((ip) => `Host IP: ${ip}`));
    }
    if (Array.isArray(parsedEvidence.interfaces)) {
      evidenceItems.push(...parsedEvidence.interfaces.map((item) => `Interface: ${item}`));
    }
    if (Array.isArray(parsedEvidence.down_interfaces)) {
      evidenceItems.push(...parsedEvidence.down_interfaces.map((item) => `Down Interface: ${item}`));
    }
    if (Array.isArray(parsedEvidence.networks)) {
      evidenceItems.push(...parsedEvidence.networks.map((item) => `Network: ${item}`));
    }
    if (Array.isArray(parsedEvidence.vlan_ids)) {
      evidenceItems.push(...parsedEvidence.vlan_ids.map((item) => `VLAN: ${item}`));
    }
    evidence = evidenceItems;
  }

  // Recommended Action
  const recommendedAction =
    intelligence?.recommended_action ||
    diagnosis?.recommended_action ||
    (primaryIssue?.details ||
      "Inspect the supplied network evidence and verify the affected configuration.");

  // Recommended Command
  const recommendedCommand =
    intelligence?.recommended_next_command ||
    intelligence?.command ||
    diagnosis?.recommended_next_command ||
    diagnosis?.recommended_command ||
    "show ip interface";

  // Additional Commands
  const recommendedCommands = Array.isArray(intelligence?.recommended_commands)
    ? intelligence.recommended_commands
    : Array.isArray(diagnosis?.recommended_commands)
    ? diagnosis.recommended_commands
    : [];

  // Explanation
  const explanation =
    intelligence?.explanation ||
    diagnosis?.explanation ||
    (primaryIssue
      ? `NetSage AI identified ${primaryIssue.check} as the primary network issue based on the supplied Cisco evidence.`
      : "NetSage AI analyzed the supplied network evidence but did not identify a deterministic configuration issue.");

  // Validation Summary
  const backendValidation =
    intelligence?.validation_summary || diagnosis?.validation_summary || null;

  const issuesDetected =
    backendValidation?.issues_detected ??
    ruleChecker?.issues_found ??
    ruleResults.filter((result) => result?.status === "ISSUE").length;

  const checksPassed =
    backendValidation?.checks_passed ??
    ruleResults.filter((result) => result?.status === "PASS").length;

  const validationStatus =
    backendValidation?.overall_status ||
    ruleChecker?.overall_status ||
    (issuesDetected > 0
      ? "ISSUES_DETECTED"
      : diagnosis
      ? "NO_ISSUES_DETECTED"
      : "UNKNOWN");

  // =====================================================
  // RENDER
  // =====================================================

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      {/* =================================================
          TOP NAVIGATION
      ================================================= */}
      <header className="h-16 border-b border-slate-800 bg-slate-950/95 px-6 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="h-9 w-9 rounded-lg bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center">
            <Network className="h-5 w-5 text-cyan-400" />
          </div>

          <div>
            <h1 className="text-lg font-bold tracking-wide">
              NetSage <span className="text-cyan-400">AI</span>
            </h1>
            <p className="text-[11px] text-slate-500">
              Network Troubleshooting Intelligence
            </p>
          </div>
        </div>

        <div className="flex items-center gap-5 text-sm text-slate-400">
          <div className="flex items-center gap-2">
            <Activity className="h-4 w-4 text-emerald-400" />
            System Online
          </div>

          <button className="hover:text-white transition">
            <Settings className="h-5 w-5" />
          </button>
        </div>
      </header>

      {/* =================================================
          APPLICATION BODY
      ================================================= */}
      <div className="flex min-h-[calc(100vh-4rem)]">
        {/* =================================================
            SIDEBAR
        ================================================= */}
        <aside className="w-64 border-r border-slate-800 bg-slate-950 p-4">
          <div className="mb-6">
            <p className="px-3 text-[11px] font-semibold uppercase tracking-wider text-slate-600">
              Workspace
            </p>
          </div>

          <nav className="space-y-1">
            <SidebarItem icon={<LayoutDashboard />} label="Dashboard" active />
            <SidebarItem icon={<BrainCircuit />} label="New Diagnosis" />
            <SidebarItem icon={<FileSearch />} label="Troubleshooting Cases" />
            <SidebarItem icon={<History />} label="Diagnosis History" />
          </nav>

          <div className="my-6 border-t border-slate-800" />

          <p className="px-3 mb-3 text-[11px] font-semibold uppercase tracking-wider text-slate-600">
            System
          </p>

          <nav className="space-y-1">
            <SidebarItem icon={<ShieldCheck />} label="Rule Checker" />
            <SidebarItem icon={<UserCheck />} label="Human Review" />
          </nav>

          <div className="mt-8 rounded-xl border border-cyan-500/20 bg-cyan-500/5 p-4">
            <div className="flex items-center gap-2 mb-2">
              <ShieldCheck className="h-4 w-4 text-cyan-400" />
              <span className="text-sm font-semibold">Human Oversight</span>
            </div>
            <p className="text-xs leading-5 text-slate-500">
              AI recommendations require human review before a diagnosis is accepted.
            </p>
          </div>
        </aside>

        {/* =================================================
            MAIN CONTENT
        ================================================= */}
        <main className="flex-1 overflow-auto">
          <div className="max-w-6xl mx-auto p-8">
            {/* PAGE HEADER */}
            <div className="mb-8">
              <div className="flex items-center gap-2 text-sm text-cyan-400 mb-2">
                <BrainCircuit className="h-4 w-4" />
                AI Troubleshooting Assistant
              </div>
              <h2 className="text-3xl font-bold tracking-tight">
                Diagnose a Network Problem
              </h2>
              <p className="mt-2 max-w-2xl text-slate-400">
                Provide the observed symptoms, topology information, and Cisco command
                evidence. NetSage AI will analyze the case and recommend the next
                troubleshooting step.
              </p>
            </div>

            {/* STATUS CARDS */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
              <StatusCard
                icon={<BrainCircuit />}
                title="AI Diagnosis"
                value={
                  loading
                    ? "Analyzing"
                    : diagnosis
                    ? "Complete"
                    : "Ready"
                }
                description="Evidence-based analysis"
              />

              <StatusCard
                icon={<Terminal />}
                title="Rule Checker"
                value={
                  diagnosis
                    ? `${issuesDetected} issue${issuesDetected === 1 ? "" : "s"}`
                    : "Ready"
                }
                description={
                  diagnosis
                    ? `${checksPassed} validation checks passed`
                    : "Deterministic validation"
                }
              />

              <StatusCard
                icon={<UserCheck />}
                title="Human Review"
                value={
                  reviewStatus === "accepted"
                    ? "Accepted"
                    : reviewStatus === "edited"
                    ? "Edited"
                    : reviewStatus === "rejected"
                    ? "Rejected"
                    : "Required"
                }
                description="Approval before acceptance"
              />
            </div>

            {/* ERROR */}
            {error && (
              <div className="mb-6 rounded-xl border border-red-500/30 bg-red-500/10 p-4">
                <div className="flex items-center gap-3">
                  <AlertTriangle className="h-5 w-5 text-red-400" />
                  <p className="text-sm text-red-300">{error}</p>
                </div>
              </div>
            )}

            {/* DIAGNOSIS FORM */}
            <div className="rounded-2xl border border-slate-800 bg-slate-900/60 shadow-xl">
              <div className="border-b border-slate-800 px-6 py-5">
                <div className="flex items-center gap-3">
                  <div className="h-10 w-10 rounded-lg bg-cyan-500/10 flex items-center justify-center">
                    <Network className="h-5 w-5 text-cyan-400" />
                  </div>
                  <div>
                    <h3 className="font-semibold">Network Case Evidence</h3>
                    <p className="text-sm text-slate-500">
                      All fields help improve diagnosis accuracy.
                    </p>
                  </div>
                </div>
              </div>

              <div className="p-6 space-y-6">
                {/* SYMPTOM */}
                <div>
                  <label className="block text-sm font-medium mb-2">
                    Network Symptom
                  </label>
                  <textarea
                    value={symptom}
                    onChange={(e) => setSymptom(e.target.value)}
                    placeholder="Example: PC receives an IP address but cannot reach the server in VLAN 30..."
                    className="w-full min-h-32 rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-slate-200 placeholder:text-slate-600 outline-none focus:border-cyan-500/60 focus:ring-2 focus:ring-cyan-500/10 transition resize-y"
                  />
                </div>

                {/* TOPOLOGY */}
                <div>
                  <label className="block text-sm font-medium mb-2">
                    Topology Notes
                  </label>
                  <textarea
                    value={topology}
                    onChange={(e) => setTopology(e.target.value)}
                    placeholder="Describe the topology, VLANs, devices, interfaces, addressing, or relevant configuration..."
                    className="w-full min-h-28 rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-slate-200 placeholder:text-slate-600 outline-none focus:border-cyan-500/60 focus:ring-2 focus:ring-cyan-500/10 transition resize-y"
                  />
                </div>

                {/* CISCO OUTPUT */}
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="block text-sm font-medium">
                      Cisco Show-Command Output
                    </label>
                    <span className="text-xs text-slate-600">Evidence</span>
                  </div>
                  <textarea
                    value={showOutput}
                    onChange={(e) => setShowOutput(e.target.value)}
                    placeholder={`show ip route\nshow interfaces\nshow vlan brief\nshow access-lists`}
                    className="w-full min-h-44 rounded-xl border border-slate-700 bg-black px-4 py-3 text-sm font-mono text-emerald-400 placeholder:text-slate-700 outline-none focus:border-cyan-500/60 focus:ring-2 focus:ring-cyan-500/10 transition resize-y"
                  />
                </div>

                {/* ACTION BAR */}
                <div className="flex items-center justify-between pt-2">
                  <div className="flex items-center gap-2 text-xs text-slate-500">
                    <AlertTriangle className="h-4 w-4" />
                    AI output must be reviewed by a human.
                  </div>

                  <div className="flex items-center gap-3">
                    <button
                      onClick={handleReset}
                      disabled={loading}
                      className="flex items-center gap-2 rounded-xl border border-slate-700 px-4 py-3 text-sm text-slate-400 hover:bg-slate-800 hover:text-white transition disabled:opacity-50"
                    >
                      <RefreshCw className="h-4 w-4" />
                      Clear
                    </button>

                    <button
                      onClick={handleAnalyze}
                      disabled={loading}
                      className="flex items-center gap-2 rounded-xl bg-cyan-500 px-5 py-3 text-sm font-semibold text-slate-950 hover:bg-cyan-400 active:scale-[0.98] transition disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {loading ? (
                        <>
                          <Activity className="h-4 w-4 animate-spin" />
                          Analyzing...
                        </>
                      ) : (
                        <>
                          Analyze Network
                          <ChevronRight className="h-4 w-4" />
                        </>
                      )}
                    </button>
                  </div>
                </div>
              </div>
            </div>

            {/* AI DIAGNOSIS RESULT */}
            {diagnosis && (
              <div className="mt-8 space-y-6">
                {/* RESULT HEADER */}
                <div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/5 p-6">
                  <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-5">
                    <div>
                      <div className="flex items-center gap-2 text-cyan-400 text-sm font-medium mb-2">
                        <BrainCircuit className="h-4 w-4" />
                        AI Diagnosis Complete
                      </div>
                      <h3 className="text-2xl font-bold">{rootCause}</h3>
                      <p className="mt-2 text-sm text-slate-400">
                        Issue Type:{" "}
                        <span className="text-slate-200">{issueType}</span>
                      </p>
                    </div>

                    <div className="rounded-xl border border-cyan-500/20 bg-slate-950/50 px-5 py-4">
                      <p className="text-xs uppercase tracking-wider text-slate-500">
                        Confidence
                      </p>
                      <p className="mt-1 text-xl font-bold text-cyan-400">
                        {confidence}
                      </p>
                    </div>
                  </div>
                </div>

                {/* ANALYSIS GRID */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Technical Reason */}
                  <ResultCard icon={<Terminal />} title="Technical Reason">
                    <p className="text-sm leading-6 text-slate-400">
                      {technicalReason}
                    </p>
                  </ResultCard>

                  {/* Evidence */}
                  <ResultCard icon={<FileSearch />} title="Supporting Evidence">
                    {Array.isArray(evidence) && evidence.length > 0 ? (
                      <div className="space-y-2">
                        {evidence.map((item, index) => (
                          <div
                            key={index}
                            className="rounded-lg border border-slate-800 bg-slate-950 px-3 py-2 text-sm font-mono text-emerald-400"
                          >
                            {typeof item === "string"
                              ? item
                              : JSON.stringify(item)}
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="text-sm text-slate-500">
                        No specific evidence was attached to the primary diagnosis.
                      </p>
                    )}
                  </ResultCard>

                  {/* Recommended Action */}
                  <ResultCard icon={<CheckCircle2 />} title="Recommended Action">
                    <p className="text-sm leading-6 text-slate-400">
                      {recommendedAction}
                    </p>
                  </ResultCard>

                  {/* Explanation */}
                  <ResultCard icon={<BrainCircuit />} title="AI Explanation">
                    <p className="text-sm leading-6 text-slate-400">
                      {explanation}
                    </p>
                  </ResultCard>
                </div>

                {/* CISCO COMMAND */}
                <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="h-10 w-10 rounded-lg bg-emerald-500/10 flex items-center justify-center">
                      <Terminal className="h-5 w-5 text-emerald-400" />
                    </div>
                    <div>
                      <h3 className="font-semibold">Recommended Cisco Command</h3>
                      <p className="text-xs text-slate-500">Next diagnostic step</p>
                    </div>
                  </div>

                  <div className="rounded-xl border border-slate-800 bg-black p-4">
                    <code className="text-sm font-mono text-emerald-400">
                      {recommendedCommand}
                    </code>
                  </div>

                  {recommendedCommands.length > 0 && (
                    <div className="mt-4">
                      <p className="text-xs uppercase tracking-wider text-slate-600 mb-2">
                        Additional Commands
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {recommendedCommands.map((command, index) => (
                          <span
                            key={index}
                            className="rounded-lg border border-slate-800 bg-slate-950 px-3 py-2 text-xs font-mono text-slate-400"
                          >
                            {command}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* VALIDATION SUMMARY */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <StatusCard
                    icon={<AlertTriangle />}
                    title="Issues Detected"
                    value={String(issuesDetected)}
                    description="Deterministic findings"
                  />
                  <StatusCard
                    icon={<CheckCircle2 />}
                    title="Checks Passed"
                    value={String(checksPassed)}
                    description="Validation checks"
                  />
                  <StatusCard
                    icon={<ShieldCheck />}
                    title="Validation Status"
                    value={validationStatus}
                    description="Rule checker result"
                  />
                </div>

                {/* RULE DETAILS */}
                {ruleResults.length > 0 && (
                  <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-6">
                    <div className="flex items-center gap-2 mb-5 text-cyan-400">
                      <ShieldCheck className="h-5 w-5" />
                      <h3 className="font-semibold text-slate-200">
                        Deterministic Validation Details
                      </h3>
                    </div>

                    <div className="space-y-3">
                      {ruleResults.map((result, index) => (
                        <div
                          key={index}
                          className="rounded-xl border border-slate-800 bg-slate-950/60 p-4"
                        >
                          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-2">
                            <div>
                              <p className="text-sm font-semibold text-slate-200">
                                {result?.check || "Validation Check"}
                              </p>
                              <p className="mt-1 text-sm text-slate-500">
                                {result?.details || "No details available."}
                              </p>
                            </div>

                            <span
                              className={`text-xs font-semibold px-3 py-1.5 rounded-lg border ${
                                result?.status === "ISSUE"
                                  ? "border-red-500/30 text-red-400 bg-red-500/10"
                                  : "border-emerald-500/30 text-emerald-400 bg-emerald-500/10"
                              }`}
                            >
                              {result?.status || "UNKNOWN"}
                            </span>
                          </div>

                          {Array.isArray(result?.evidence) &&
                            result.evidence.length > 0 && (
                              <div className="mt-3 flex flex-wrap gap-2">
                                {result.evidence.map((item, evidenceIndex) => (
                                  <span
                                    key={evidenceIndex}
                                    className="rounded-md border border-slate-800 bg-black px-2 py-1 text-xs font-mono text-emerald-400"
                                  >
                                    {typeof item === "string"
                                      ? item
                                      : JSON.stringify(item)}
                                  </span>
                                ))}
                              </div>
                            )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* HUMAN REVIEW */}
                <div className="rounded-2xl border border-amber-500/20 bg-amber-500/5 p-6">
                  <div className="flex items-start gap-4">
                    <div className="h-10 w-10 shrink-0 rounded-lg bg-amber-500/10 flex items-center justify-center">
                      <UserCheck className="h-5 w-5 text-amber-400" />
                    </div>

                    <div className="flex-1">
                      <h3 className="font-semibold text-amber-300">
                        Human Review Required
                      </h3>
                      <p className="mt-1 text-sm leading-6 text-slate-400">
                        {diagnosis?.human_review?.message ||
                          intelligence?.human_review?.reason ||
                          "Automated recommendations should be reviewed by a qualified human before any network configuration changes are accepted."}
                      </p>

                      {reviewError && (
                        <div className="mt-4 rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-3">
                          <div className="flex items-center gap-2">
                            <AlertTriangle className="h-4 w-4 text-red-400" />
                            <p className="text-sm text-red-300">{reviewError}</p>
                          </div>
                        </div>
                      )}

                      <div className="flex flex-wrap gap-3 mt-5">
                        <button
                          onClick={() => handleReview("accepted")}
                          disabled={reviewLoading}
                          className={`flex items-center gap-2 rounded-lg px-4 py-2.5 text-sm font-medium transition ${
                            reviewStatus === "accepted"
                              ? "bg-emerald-500 text-slate-950"
                              : "border border-emerald-500/30 text-emerald-400 hover:bg-emerald-500/10"
                          } disabled:opacity-50 disabled:cursor-not-allowed`}
                        >
                          <CheckCircle2 className="h-4 w-4" />
                          Accept
                        </button>

                        <button
                          onClick={() => handleReview("edited")}
                          disabled={reviewLoading}
                          className={`flex items-center gap-2 rounded-lg px-4 py-2.5 text-sm font-medium transition ${
                            reviewStatus === "edited"
                              ? "bg-cyan-500 text-slate-950"
                              : "border border-cyan-500/30 text-cyan-400 hover:bg-cyan-500/10"
                          } disabled:opacity-50 disabled:cursor-not-allowed`}
                        >
                          <Settings className="h-4 w-4" />
                          Edit / Review
                        </button>

                        <button
                          onClick={() => handleReview("rejected")}
                          disabled={reviewLoading}
                          className={`flex items-center gap-2 rounded-lg px-4 py-2.5 text-sm font-medium transition ${
                            reviewStatus === "rejected"
                              ? "bg-red-500 text-white"
                              : "border border-red-500/30 text-red-400 hover:bg-red-500/10"
                          } disabled:opacity-50 disabled:cursor-not-allowed`}
                        >
                          <XCircle className="h-4 w-4" />
                          Reject
                        </button>
                      </div>

                      {showEditReview && (
                        <div className="mt-5 rounded-xl border border-cyan-500/20 bg-slate-950/60 p-5">
                          <div className="flex items-center gap-2 mb-4">
                            <Settings className="h-4 w-4 text-cyan-400" />
                            <h4 className="font-semibold text-slate-200">
                              Edit AI Recommendation
                            </h4>
                          </div>

                          <div className="space-y-4">
                            <div>
                              <label className="block text-xs font-medium text-slate-400 mb-2">
                                Issue
                              </label>
                              <input
                                value={editedIssue}
                                onChange={(e) => setEditedIssue(e.target.value)}
                                className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2.5 text-sm text-slate-200 outline-none focus:border-cyan-500/60"
                              />
                            </div>

                            <div>
                              <label className="block text-xs font-medium text-slate-400 mb-2">
                                Root Cause
                              </label>
                              <textarea
                                value={editedRootCause}
                                onChange={(e) => setEditedRootCause(e.target.value)}
                                className="w-full min-h-24 rounded-lg border border-slate-700 bg-slate-950 px-3 py-2.5 text-sm text-slate-200 outline-none focus:border-cyan-500/60 resize-y"
                              />
                            </div>

                            <div>
                              <label className="block text-xs font-medium text-slate-400 mb-2">
                                Recommended Action
                              </label>
                              <textarea
                                value={editedAction}
                                onChange={(e) => setEditedAction(e.target.value)}
                                className="w-full min-h-24 rounded-lg border border-slate-700 bg-slate-950 px-3 py-2.5 text-sm text-slate-200 outline-none focus:border-cyan-500/60 resize-y"
                              />
                            </div>

                            <div>
                              <label className="block text-xs font-medium text-slate-400 mb-2">
                                Reviewer Note
                              </label>
                              <textarea
                                value={reviewerNote}
                                onChange={(e) => setReviewerNote(e.target.value)}
                                placeholder="Optional note explaining the review decision..."
                                className="w-full min-h-20 rounded-lg border border-slate-700 bg-slate-950 px-3 py-2.5 text-sm text-slate-200 placeholder:text-slate-600 outline-none focus:border-cyan-500/60 resize-y"
                              />
                            </div>

                            <div className="flex flex-wrap gap-3 pt-1">
                              <button
                                onClick={handleSubmitEditedReview}
                                disabled={reviewLoading}
                                className="flex items-center gap-2 rounded-lg bg-cyan-500 px-4 py-2.5 text-sm font-semibold text-slate-950 hover:bg-cyan-400 transition disabled:opacity-50 disabled:cursor-not-allowed"
                              >
                                {reviewLoading ? (
                                  <Activity className="h-4 w-4 animate-spin" />
                                ) : (
                                  <CheckCircle2 className="h-4 w-4" />
                                )}
                                Save Edited Review
                              </button>

                              <button
                                onClick={() => setShowEditReview(false)}
                                disabled={reviewLoading}
                                className="rounded-lg border border-slate-700 px-4 py-2.5 text-sm text-slate-400 hover:bg-slate-800 hover:text-white transition disabled:opacity-50"
                              >
                                Cancel
                              </button>
                            </div>
                          </div>
                        </div>
                      )}

                      {reviewStatus !== "pending" && !showEditReview && (
                        <div className="mt-4 rounded-lg border border-slate-800 bg-slate-950/60 px-4 py-3">
                          <p className="text-xs text-slate-500">Review status</p>
                          <p className="mt-1 text-sm font-medium text-slate-200">
                            {reviewStatus === "accepted"
                              ? "Diagnosis accepted by human reviewer."
                              : reviewStatus === "edited"
                              ? "Diagnosis edited and saved by human reviewer."
                              : "Diagnosis rejected by human reviewer."}
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                {/* INFO CARDS */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
                  <InfoCard
                    icon={<Clock3 />}
                    title="Evidence-Based Diagnosis"
                    text="NetSage AI uses symptoms and command evidence instead of relying only on assumptions."
                  />

                  <InfoCard
                    icon={<CheckCircle2 />}
                    title="Human-in-the-Loop"
                    text="Every diagnosis can be accepted, edited, or rejected by a human reviewer."
                  />
                </div>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}

// =========================================================
// SIDEBAR ITEM
// =========================================================

function SidebarItem({ icon, label, active = false }) {
  return (
    <button
      className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition ${
        active
          ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/20"
          : "text-slate-400 hover:bg-slate-900 hover:text-slate-200"
      }`}
    >
      <span className="h-4 w-4">{icon}</span>
      {label}
    </button>
  );
}

// =========================================================
// STATUS CARD
// =========================================================

function StatusCard({ icon, title, value, description }) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
      <div className="flex items-center gap-3">
        <div className="h-9 w-9 rounded-lg bg-cyan-500/10 text-cyan-400 flex items-center justify-center">
          {icon}
        </div>
        <div>
          <p className="text-xs text-slate-500">{title}</p>
          <p className="font-semibold">{value}</p>
        </div>
      </div>
      <p className="mt-3 text-xs text-slate-600">{description}</p>
    </div>
  );
}

// =========================================================
// RESULT CARD
// =========================================================

function ResultCard({ icon, title, children }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-6">
      <div className="flex items-center gap-2 mb-4 text-cyan-400">
        {icon}
        <h4 className="text-sm font-semibold text-slate-200">{title}</h4>
      </div>
      {children}
    </div>
  );
}

// =========================================================
// INFORMATION CARD
// =========================================================

function InfoCard({ icon, title, text }) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-5">
      <div className="flex items-center gap-2 mb-2 text-cyan-400">
        {icon}
        <h4 className="text-sm font-semibold text-slate-200">{title}</h4>
      </div>
      <p className="text-sm leading-6 text-slate-500">{text}</p>
    </div>
  );
}

export default App;