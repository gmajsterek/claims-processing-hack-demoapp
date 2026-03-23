"""
Claims Intelligence Platform - Static Demo Application
Capgemini x Azure AI | Insurance Claims Processing Demo
All data is hardcoded for demonstration purposes.
"""

import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# ──────────────────────────────────────────────────────────────────────────────
# Hardcoded demo data
# ──────────────────────────────────────────────────────────────────────────────

POLICIES = {
    "LIAB-AUTO-001": {
        "code": "LIAB-AUTO-001",
        "name": "Liability Only Auto Insurance",
        "category": "Minimum Coverage",
        "monthly_premium": 89,
        "description": "Covers damages and injuries you cause to others. Does NOT cover damage to your own vehicle.",
        "covered": [
            "Bodily injury to third parties",
            "Property damage liability",
            "Legal defence costs",
            "Third-party medical expenses"
        ],
        "not_covered": [
            "Collision damage to your own vehicle",
            "Comprehensive damage (theft, vandalism, weather)",
            "Your own medical expenses",
            "Mechanical breakdown"
        ],
        "limits": {
            "bodily_injury_per_person": "$25,000",
            "bodily_injury_per_accident": "$50,000",
            "property_damage": "$25,000"
        },
        "deductible": "N/A",
        "sections": ["2.1 Bodily Injury Liability", "2.2 Property Damage Liability", "4.1 Own Vehicle Exclusion"]
    },
    "COMM-AUTO-001": {
        "code": "COMM-AUTO-001",
        "name": "Commercial Auto Insurance",
        "category": "Business Vehicle Coverage",
        "monthly_premium": 312,
        "description": "Comprehensive coverage for vehicles used in business operations, including collision, comprehensive, and liability.",
        "covered": [
            "Collision damage during business use",
            "Comprehensive coverage (theft, weather, fire)",
            "Liability to third parties",
            "Medical payments for employees",
            "Towing and roadside assistance",
            "Rental reimbursement"
        ],
        "not_covered": [
            "Racing or competition use",
            "Intentional damage",
            "DUI-related incidents",
            "Nuclear hazards"
        ],
        "limits": {
            "collision": "$50,000 per incident",
            "comprehensive": "$50,000 per incident",
            "liability": "$1,000,000 per accident"
        },
        "deductible": "$500",
        "sections": ["Collision Coverage", "Comprehensive Coverage", "Medical Payments", "Uninsured Motorist"]
    },
    "COMP-AUTO-001": {
        "code": "COMP-AUTO-001",
        "name": "Comprehensive Auto Insurance",
        "category": "Full Coverage",
        "monthly_premium": 198,
        "description": "Full coverage including collision, comprehensive, and liability protection for personal vehicles.",
        "covered": [
            "Collision damage",
            "Theft and vandalism",
            "Weather-related damage",
            "Fire damage",
            "Third-party liability",
            "Medical payments"
        ],
        "not_covered": [
            "Racing events",
            "Intentional damage",
            "Wear and tear",
            "DUI incidents"
        ],
        "limits": {
            "collision": "$30,000",
            "comprehensive": "$30,000",
            "liability": "$500,000"
        },
        "deductible": "$750",
        "sections": ["Collision Coverage", "Comprehensive Coverage", "Liability", "Medical Payments"]
    },
    "HV-AUTO-001": {
        "code": "HV-AUTO-001",
        "name": "High Value Vehicle Insurance",
        "category": "Premium Coverage",
        "monthly_premium": 485,
        "description": "Tailored insurance for luxury and exotic vehicles with agreed value coverage and concierge claims service.",
        "covered": [
            "Agreed value collision coverage",
            "Comprehensive protection",
            "Worldwide coverage",
            "Original equipment parts guarantee",
            "Concierge claims service",
            "Track day coverage (limited)"
        ],
        "not_covered": [
            "Competition racing",
            "Deliberate damage",
            "Commercial hire"
        ],
        "limits": {
            "agreed_value": "Up to $500,000",
            "liability": "$2,000,000"
        },
        "deductible": "$1,000",
        "sections": ["Agreed Value Coverage", "Worldwide Protection", "Premium Services"]
    },
    "MOTO-001": {
        "code": "MOTO-001",
        "name": "Motorcycle Insurance",
        "category": "Specialty Vehicle",
        "monthly_premium": 124,
        "description": "Comprehensive motorcycle insurance including gear coverage, roadside assistance, and liability protection.",
        "covered": [
            "Collision damage",
            "Theft and vandalism",
            "Rider gear coverage (up to $2,000)",
            "Roadside assistance",
            "Third-party liability",
            "Trip interruption coverage"
        ],
        "not_covered": [
            "Racing events",
            "Off-road use",
            "Commercial delivery",
            "DUI incidents"
        ],
        "limits": {
            "collision": "$20,000",
            "comprehensive": "$20,000",
            "liability": "$300,000"
        },
        "deductible": "$500",
        "sections": ["Collision Coverage", "Gear Coverage", "Roadside Assistance", "Liability"]
    }
}

CLAIMS = {
    "crash1": {
        "id": "crash1",
        "claim_number": "CLM-2025-52814",
        "status": "denied",
        "submitted_date": "2025-07-17",
        "processed_date": "2025-07-17",
        "processing_time_seconds": 2.1,
        "claimant": {
            "name": "John Peterson",
            "phone": "(937) 555-2319",
            "address": "1142 Pinecrest Avenue, Springfield, OH 45503",
            "email": "john.peterson@email.com"
        },
        "vehicle": {
            "year": 2004,
            "make": "Honda",
            "model": "Accord",
            "color": "Silver",
            "vin": "1HGCM56404A123456",
            "plate": "OH-GHR1984"
        },
        "policy": {
            "number": "LIAB-AUTO-001",
            "type": "Liability Only Auto Insurance"
        },
        "incident": {
            "date": "July 17, 2025",
            "time": "8:30 AM",
            "location": "Parking lot, 2325 Main Street, Springfield, OH 45503",
            "description": "Vehicle legally parked in marked space. Gray pickup truck attempting to park beside struck the front end and driver's side of vehicle causing significant damage. Other driver left information and waited for police.",
            "police_report": "25-52814",
            "weather": "Clear"
        },
        "damage": {
            "description": "Front bumper dislodged and partially detached; severe denting and scraping on driver's side front quarter panel; wheel and tire on driver's side front damaged; paint transfer and deformity on the driver's door; headlamp assembly and grille potentially damaged.",
            "severity": "moderate",
            "estimated_repair_cost": 4850,
            "affected_areas": ["Front bumper", "Driver's side quarter panel", "Front wheel & tire", "Driver's door", "Headlamp assembly"]
        },
        "claim_request": "Full coverage of repair expenses minus deductible",
        "pipeline": {
            "ocr": {
                "model": "Mistral Document AI",
                "confidence": 0.97,
                "characters_extracted": 843,
                "text_preview": "ACCIDENT STATEMENT FORM\n\nPolicyholder: John Peterson\nPolicy Number: LIAB-AUTO-001\nDate of Incident: July 17, 2025\nTime: 8:30 AM\nLocation: Parking Lot, 2325 Main Street, Springfield, OH 45503\n\nVehicle: 2004 Honda Accord | Silver | VIN: 1HGCM56404A123456\nLicense Plate: OH-GHR1984\n\nDescription: Vehicle was legally parked. Gray pickup truck struck front end and driver's side causing significant damage. Other driver provided information...",
                "processing_ms": 420
            },
            "structuring": {
                "model": "GPT-4.1-mini",
                "fields_extracted": 16,
                "confidence": 0.99,
                "processing_ms": 780
            },
            "policy_match": {
                "model": "Azure AI Search + GPT-4.1-mini",
                "search_results": 1,
                "match_confidence": 1.0,
                "policy_found": "LIAB-AUTO-001 - Liability Only Auto Insurance",
                "processing_ms": 340
            },
            "coverage_validation": {
                "model": "GPT-4.1-mini",
                "sections_checked": ["Section 2.1", "Section 2.2", "Section 4.1"],
                "exclusions_checked": ["Section 4.1 - Own vehicle collision damage", "Section 4.3 - Additional exclusions"],
                "processing_ms": 560
            }
        },
        "decision": {
            "outcome": "DENIED",
            "applicable_coverage": "None - Own vehicle damage not covered",
            "deductible": None,
            "coverage_limit": None,
            "payout_estimate": 0,
            "reasoning": "The policyholder holds a Liability Only policy (LIAB-AUTO-001), which explicitly does NOT cover damage to the policyholder's own vehicle. Section 4.1 states: 'Collision damage to your vehicle' is excluded. The claimant's request for repair coverage of their 2004 Honda Accord cannot be fulfilled under this policy. The claimant should file against the at-fault driver's insurance instead.",
            "exclusions_triggered": ["Section 4.1 - Collision damage to own vehicle excluded"],
            "recommendation": "Advise claimant to file against at-fault driver's liability insurance. Consider upgrading to comprehensive or collision coverage."
        }
    },

    "crash2": {
        "id": "crash2",
        "claim_number": "CLM-2025-13982",
        "status": "approved",
        "submitted_date": "2025-07-18",
        "processed_date": "2025-07-18",
        "processing_time_seconds": 2.4,
        "claimant": {
            "name": "Samantha Turner",
            "phone": "(518) 555-2913",
            "address": "507 Walnut Lane, Albany, NY 12208",
            "email": "s.turner@businessmail.com"
        },
        "vehicle": {
            "year": 2017,
            "make": "Honda",
            "model": "Civic Hatchback",
            "color": "Blue-Gray",
            "vin": "19XFC2F5XHE200487",
            "plate": "NY-FZX1452"
        },
        "policy": {
            "number": "COMM-AUTO-001",
            "type": "Commercial Auto Insurance"
        },
        "incident": {
            "date": "July 18, 2025",
            "time": "4:10 PM",
            "location": "2100 Madison Avenue, Albany, NY 12208",
            "description": "Driving eastbound through green light when another vehicle traveling southbound failed to stop at red signal and struck vehicle on driver's side. Car spun partially before stopping near curb. Other driver admitted fault to police.",
            "police_report": "25-13982",
            "weather": "Clear"
        },
        "damage": {
            "description": "Heavy intrusion and bending on driver's front and rear doors; B-pillar area severely compromised; rear wheel misaligned; shattered rear driver's side window; deployment of side airbags; vehicle towed from accident location.",
            "severity": "severe",
            "estimated_repair_cost": 18750,
            "affected_areas": ["Driver's doors (front & rear)", "B-pillar", "Rear wheel", "Side windows", "Airbags"]
        },
        "claim_request": "Assessment and full coverage for extensive body and structural repairs",
        "pipeline": {
            "ocr": {
                "model": "Mistral Document AI",
                "confidence": 0.98,
                "characters_extracted": 912,
                "text_preview": "ACCIDENT STATEMENT FORM\n\nPolicyholder: Samantha Turner\nPolicy Number: COMM-AUTO-001\nDate of Incident: July 18, 2025\nTime: 4:10 PM\nLocation: 2100 Madison Avenue, Albany, NY 12208\n\nVehicle: 2017 Honda Civic Hatchback | Blue-Gray | VIN: 19XFC2F5XHE200487\n\nDescription: Driving eastbound through green light when other vehicle ran red signal and struck driver's side. Side airbags deployed. Vehicle towed from scene...",
                "processing_ms": 390
            },
            "structuring": {
                "model": "GPT-4.1-mini",
                "fields_extracted": 17,
                "confidence": 0.99,
                "processing_ms": 810
            },
            "policy_match": {
                "model": "Azure AI Search + GPT-4.1-mini",
                "search_results": 1,
                "match_confidence": 1.0,
                "policy_found": "COMM-AUTO-001 - Commercial Auto Insurance",
                "processing_ms": 320
            },
            "coverage_validation": {
                "model": "GPT-4.1-mini",
                "sections_checked": ["Collision Coverage", "Comprehensive Coverage", "Medical Payments"],
                "exclusions_checked": ["Racing exclusion", "DUI exclusion", "Intentional damage"],
                "processing_ms": 480
            }
        },
        "decision": {
            "outcome": "APPROVED",
            "applicable_coverage": "Physical Damage - Collision Coverage",
            "deductible": "$500",
            "coverage_limit": "$50,000 per incident",
            "payout_estimate": 18250,
            "reasoning": "The claim involves collision damage sustained during normal business driving operations. The policyholder holds a Commercial Auto policy (COMM-AUTO-001) which includes Physical Damage – Collision Coverage for 'Damage from vehicle collisions during business use'. The other driver ran a red light and admitted fault. No policy exclusions apply. Towing costs are also covered under the policy.",
            "exclusions_triggered": [],
            "recommendation": "Approve claim. Estimated payout: $18,250 (repair cost $18,750 minus $500 deductible). Initiate subrogation against at-fault driver."
        }
    },

    "crash3": {
        "id": "crash3",
        "claim_number": "CLM-2025-44278",
        "status": "denied",
        "submitted_date": "2025-07-19",
        "processed_date": "2025-07-19",
        "processing_time_seconds": 1.9,
        "claimant": {
            "name": "Michael Rodriguez",
            "phone": "(717) 555-7745",
            "address": "217 Maplewood Avenue, Harrisburg, PA 17102",
            "email": "m.rodriguez@personal.com"
        },
        "vehicle": {
            "year": 2012,
            "make": "Suzuki",
            "model": "SX4",
            "color": "White",
            "vin": "JS2YB5A31C6109734",
            "plate": "PA-KLX2194"
        },
        "policy": {
            "number": "LIAB-AUTO-001",
            "type": "Liability Only Auto Insurance"
        },
        "incident": {
            "date": "July 19, 2025",
            "time": "6:30 PM",
            "location": "400 East 8th Street, Harrisburg, PA 17102",
            "description": "Operating vehicle eastbound, slowed to make left turn. Another vehicle at excessive speed attempted to overtake on left and collided with rear driver's side. Impact caused car to spin and strike nearby curb. At-fault driver admitted fault.",
            "police_report": "25-44278",
            "weather": "Partly cloudy, dry roads"
        },
        "damage": {
            "description": "Major denting to rear driver's side quarter panel and bumper; front bumper heavily crumpled due to curb impact; left front wheel and suspension suspected damaged; vehicle not drivable, towed for assessment.",
            "severity": "severe",
            "estimated_repair_cost": 6200,
            "affected_areas": ["Rear quarter panel", "Rear bumper", "Front bumper", "Left front wheel", "Suspension"]
        },
        "claim_request": "Full assessment and repair of all damage to rear quarter panel, front bumper, and suspension",
        "pipeline": {
            "ocr": {
                "model": "Mistral Document AI",
                "confidence": 0.96,
                "characters_extracted": 798,
                "text_preview": "ACCIDENT STATEMENT FORM\n\nPolicyholder: Michael Rodriguez\nPolicy Number: LIAB-AUTO-001\nDate of Incident: July 19, 2025\nTime: 6:30 PM\nLocation: 400 East 8th Street, Harrisburg, PA 17102\n\nVehicle: 2012 Suzuki SX4 | White | VIN: JS2YB5A31C6109734\n\nDescription: Slowing for left turn when speeding vehicle overtook from left, striking rear driver's side. Impact spun vehicle into curb causing additional front damage...",
                "processing_ms": 410
            },
            "structuring": {
                "model": "GPT-4.1-mini",
                "fields_extracted": 16,
                "confidence": 0.98,
                "processing_ms": 720
            },
            "policy_match": {
                "model": "Azure AI Search + GPT-4.1-mini",
                "search_results": 1,
                "match_confidence": 1.0,
                "policy_found": "LIAB-AUTO-001 - Liability Only Auto Insurance",
                "processing_ms": 310
            },
            "coverage_validation": {
                "model": "GPT-4.1-mini",
                "sections_checked": ["Section 2.1", "Section 2.2", "Section 4.1"],
                "exclusions_checked": ["Section 4.1 - Own vehicle collision damage"],
                "processing_ms": 450
            }
        },
        "decision": {
            "outcome": "DENIED",
            "applicable_coverage": "None - Own vehicle damage not covered",
            "deductible": None,
            "coverage_limit": None,
            "payout_estimate": 0,
            "reasoning": "Same scenario as prior liability-only claims. The policyholder's Liability Only policy (LIAB-AUTO-001) does not cover damage to their own vehicle. Although the other driver was at fault, the policyholder's own policy cannot pay for repairs to their 2012 Suzuki SX4. Section 4.1 explicitly excludes 'Collision damage to your vehicle'. The claimant must seek compensation from the at-fault driver's insurance.",
            "exclusions_triggered": ["Section 4.1 - Collision damage to own vehicle excluded"],
            "recommendation": "Deny claim. Advise claimant to file against at-fault driver's liability coverage. Provide information on how to upgrade to comprehensive policy."
        }
    },

    "crash4": {
        "id": "crash4",
        "claim_number": "CLM-2025-22097",
        "status": "approved",
        "submitted_date": "2025-07-19",
        "processed_date": "2025-07-19",
        "processing_time_seconds": 2.6,
        "claimant": {
            "name": "Andrea M. Bennett",
            "phone": "(937) 555-2319",
            "address": "1142 Pinecrest Avenue, Springfield, OH 45503",
            "email": "a.bennett@company.com"
        },
        "vehicle": {
            "year": 2011,
            "make": "Subaru",
            "model": "Outback",
            "color": "Red",
            "vin": "4S4BRBCC2B3378210",
            "plate": "OH-CRV4413"
        },
        "policy": {
            "number": "COMM-AUTO-001",
            "type": "Commercial Auto Insurance"
        },
        "incident": {
            "date": "July 19, 2025",
            "time": "11:15 AM",
            "location": "6400 Westbrook Road, Dayton, OH 45415",
            "description": "Driving westbound, waiting in traffic for stop sign. Vehicle was rear-ended by blue sedan at moderate speed. Impact pushed vehicle into adjacent lane. Other driver remained at scene and called authorities.",
            "police_report": "25-22097",
            "weather": "Clear, dry roads"
        },
        "damage": {
            "description": "Severe crumpling to rear bumper and rear quarter panel; rear taillight broken; rear hatch door bent and misaligned; suspension may be compromised; rear wheel not tracking properly; possible interior damage.",
            "severity": "severe",
            "estimated_repair_cost": 9400,
            "affected_areas": ["Rear bumper", "Rear quarter panel", "Taillight assembly", "Rear hatch", "Suspension"]
        },
        "claim_request": "Assessment and coverage for all rear-end bodywork and mechanical repairs, plus reimbursement for towing costs",
        "pipeline": {
            "ocr": {
                "model": "Mistral Document AI",
                "confidence": 0.97,
                "characters_extracted": 856,
                "text_preview": "ACCIDENT STATEMENT FORM\n\nPolicyholder: Andrea M. Bennett\nPolicy Number: COMM-AUTO-001\nDate of Incident: July 19, 2025\nTime: 11:15 AM\nLocation: 6400 Westbrook Road, Dayton, OH 45415\n\nVehicle: 2011 Subaru Outback | Red | VIN: 4S4BRBCC2B3378210\n\nDescription: Waiting in traffic when rear-ended by blue sedan. Significant rear-end damage, vehicle pushed into adjacent lane...",
                "processing_ms": 440
            },
            "structuring": {
                "model": "GPT-4.1-mini",
                "fields_extracted": 17,
                "confidence": 0.99,
                "processing_ms": 800
            },
            "policy_match": {
                "model": "Azure AI Search + GPT-4.1-mini",
                "search_results": 1,
                "match_confidence": 1.0,
                "policy_found": "COMM-AUTO-001 - Commercial Auto Insurance",
                "processing_ms": 350
            },
            "coverage_validation": {
                "model": "GPT-4.1-mini",
                "sections_checked": ["Collision Coverage", "Towing & Roadside"],
                "exclusions_checked": ["Racing exclusion", "DUI exclusion"],
                "processing_ms": 510
            }
        },
        "decision": {
            "outcome": "APPROVED",
            "applicable_coverage": "Physical Damage - Collision Coverage + Towing Reimbursement",
            "deductible": "$500",
            "coverage_limit": "$50,000 per incident",
            "payout_estimate": 9200,
            "reasoning": "Rear-end collision during business operations is covered under the Commercial Auto policy (COMM-AUTO-001) Physical Damage – Collision Coverage. Towing costs are also covered under the roadside assistance component. No policy exclusions apply. Other driver remained at scene and report was filed.",
            "exclusions_triggered": [],
            "recommendation": "Approve claim. Estimated payout: $9,200 (repair $9,400 - $500 deductible + estimated towing ~$300). Initiate subrogation against at-fault driver."
        }
    },

    "crash5": {
        "id": "crash5",
        "claim_number": "CLM-2025-33109",
        "status": "approved",
        "submitted_date": "2025-07-19",
        "processed_date": "2025-07-19",
        "processing_time_seconds": 2.3,
        "claimant": {
            "name": "Christopher J. Ryan",
            "phone": "(614) 555-3791",
            "address": "338 Willow Crest Drive, Columbus, OH 43214",
            "email": "c.ryan@workmail.com"
        },
        "vehicle": {
            "year": 2016,
            "make": "Toyota",
            "model": "Corolla",
            "color": "Black",
            "vin": "2T1BURHE1GC123905",
            "plate": "OH-TLY3829"
        },
        "policy": {
            "number": "COMM-AUTO-001",
            "type": "Commercial Auto Insurance"
        },
        "incident": {
            "date": "July 19, 2025",
            "time": "2:50 PM",
            "location": "Intersection of Karl Road & Bethel Road, Columbus, OH 43214",
            "description": "Driving eastbound on Bethel Road, entered intersection at Karl Road. Gray pickup truck traveling northbound failed to yield while making left turn and struck rear driver's side. Impact spun car, causing extensive damage.",
            "police_report": "25-33109",
            "weather": "Clear, dry pavement"
        },
        "damage": {
            "description": "Severe crumpling of left rear quarter panel and bumper; rear taillight shattered; rear door and trunk misaligned; rear wheel bent with suspected axle damage; possible undercarriage and suspension issues; vehicle towed from scene.",
            "severity": "severe",
            "estimated_repair_cost": 11300,
            "affected_areas": ["Left rear quarter panel", "Rear bumper", "Taillight", "Rear door/trunk", "Rear axle", "Suspension"]
        },
        "claim_request": "Full assessment and coverage for all necessary body, mechanical, and suspension repairs, plus reimbursement for towing costs",
        "pipeline": {
            "ocr": {
                "model": "Mistral Document AI",
                "confidence": 0.98,
                "characters_extracted": 881,
                "text_preview": "ACCIDENT STATEMENT FORM\n\nPolicyholder: Christopher J. Ryan\nPolicy Number: COMM-AUTO-001\nDate of Incident: July 19, 2025\nTime: 2:50 PM\nLocation: Intersection Karl Road & Bethel Road, Columbus, OH 43214\n\nVehicle: 2016 Toyota Corolla | Black | VIN: 2T1BURHE1GC123905\n\nDescription: Entered intersection on green, pickup truck failed to yield on left turn and struck rear driver's side. Car spun. Significant structural damage...",
                "processing_ms": 400
            },
            "structuring": {
                "model": "GPT-4.1-mini",
                "fields_extracted": 17,
                "confidence": 0.99,
                "processing_ms": 790
            },
            "policy_match": {
                "model": "Azure AI Search + GPT-4.1-mini",
                "search_results": 1,
                "match_confidence": 1.0,
                "policy_found": "COMM-AUTO-001 - Commercial Auto Insurance",
                "processing_ms": 330
            },
            "coverage_validation": {
                "model": "GPT-4.1-mini",
                "sections_checked": ["Collision Coverage", "Comprehensive Coverage", "Towing & Roadside"],
                "exclusions_checked": ["Racing exclusion", "DUI exclusion", "Intentional damage"],
                "processing_ms": 530
            }
        },
        "decision": {
            "outcome": "APPROVED",
            "applicable_coverage": "Physical Damage - Collision Coverage + Towing Reimbursement",
            "deductible": "$500",
            "coverage_limit": "$50,000 per incident",
            "payout_estimate": 11100,
            "reasoning": "Intersection collision where other driver failed to yield is covered under Commercial Auto policy (COMM-AUTO-001) Physical Damage – Collision Coverage. Towing and axle/suspension repairs are all within scope. No exclusions apply. Police report filed and other driver remained at scene.",
            "exclusions_triggered": [],
            "recommendation": "Approve claim. Estimated payout: $11,100 (repair $11,300 - $500 deductible + towing ~$300). Initiate subrogation against at-fault driver."
        }
    }
}

# ──────────────────────────────────────────────────────────────────────────────
# FastAPI Application
# ──────────────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Claims Intelligence Platform",
    description="Capgemini x Azure AI – Insurance Claims Processing Demo",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
IMAGES_DIR = BASE_DIR.parent / "challenge-0" / "data" / "images"


# ── Static / Root ──────────────────────────────────────────────────────────────
@app.get("/")
async def root():
    return FileResponse(str(STATIC_DIR / "index.html"))


@app.get("/images/{filename}")
async def get_image(filename: str):
    """Serve crash images from challenge-0/data/images."""
    # Sanitize filename to prevent path traversal
    safe_name = Path(filename).name
    image_path = IMAGES_DIR / safe_name
    if image_path.exists():
        return FileResponse(str(image_path))
    raise HTTPException(status_code=404, detail="Image not found")


# ── API endpoints ──────────────────────────────────────────────────────────────
@app.get("/api/stats")
async def get_stats():
    total = len(CLAIMS)
    approved = sum(1 for c in CLAIMS.values() if c["status"] == "approved")
    denied = sum(1 for c in CLAIMS.values() if c["status"] == "denied")
    total_payout = sum(c["decision"]["payout_estimate"] for c in CLAIMS.values())
    avg_time = round(
        sum(c["processing_time_seconds"] for c in CLAIMS.values()) / total, 1
    )
    return {
        "total_claims": total,
        "approved": approved,
        "denied": denied,
        "pending": 0,
        "approval_rate": round(approved / total * 100),
        "avg_processing_seconds": avg_time,
        "total_payout_estimate": total_payout,
        "accuracy_rate": 98.5,
        "annual_savings_estimate": 847000,
        "manual_processing_days": 3,
        "ai_processing_seconds": avg_time,
    }


@app.get("/api/claims")
async def list_claims():
    summary = []
    for c in CLAIMS.values():
        summary.append({
            "id": c["id"],
            "claim_number": c["claim_number"],
            "status": c["status"],
            "claimant_name": c["claimant"]["name"],
            "vehicle": f"{c['vehicle']['year']} {c['vehicle']['make']} {c['vehicle']['model']}",
            "policy_number": c["policy"]["number"],
            "policy_type": c["policy"]["type"],
            "incident_date": c["incident"]["date"],
            "damage_severity": c["damage"]["severity"],
            "estimated_cost": c["damage"]["estimated_repair_cost"],
            "decision": c["decision"]["outcome"],
            "submitted_date": c["submitted_date"],
        })
    return summary


@app.get("/api/claims/{claim_id}")
async def get_claim(claim_id: str):
    if claim_id not in CLAIMS:
        raise HTTPException(status_code=404, detail="Claim not found")
    return CLAIMS[claim_id]


@app.get("/api/policies")
async def list_policies():
    return list(POLICIES.values())


@app.get("/api/policies/{policy_code}")
async def get_policy(policy_code: str):
    if policy_code not in POLICIES:
        raise HTTPException(status_code=404, detail="Policy not found")
    return POLICIES[policy_code]


# ── Static files (must be last so routes take priority) ───────────────────────
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
