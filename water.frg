#lang forge/temporal
// option bitwidth 6

// Our discrete states for water quality and plant growth
abstract sig WaterQualityState {}
one sig Low extends WaterQualityState {}
one sig Medium extends WaterQualityState {}
one sig High extends WaterQualityState {}

// Abstract signature to group plant growth states
abstract sig PlantGrowthState {}
one sig Sparse extends PlantGrowthState {}
one sig Moderate extends PlantGrowthState {}
one sig Dense extends PlantGrowthState {}

// Signature for mussel population thresholds
abstract sig MusselPopulation {}
one sig LowPopulation extends MusselPopulation {}
one sig MediumPopulation extends MusselPopulation {}
one sig HighPopulation extends MusselPopulation {}

abstract sig Boolean {}
one sig True, False extends Boolean {}

// Signature for Zebra Mussels with a property to indicate whether they are juveniles or adults
sig ZebraMussel {
    //if a mussel is juvenile, it filters less water
    var isJuvenile: one Boolean
}

// Signature for Water Quality using discrete states
sig WaterQuality {
    var clarity: one WaterQualityState
}

// Signature for Plant Growth using discrete states
sig PlantGrowth {
    var growthState: one PlantGrowthState
}

// Main model signature for a Lake that contains Zebra Mussels, Water Quality, and Plant Growth
sig Lake {
    var mussels: set ZebraMussel,
    var waterQuality: one WaterQuality,
    var plants: one PlantGrowth,
    var musselPopulation: one MusselPopulation
}

// Initial conditions: Assuming the lake starts with medium water clarity and moderate plant growth
// pred initConditions {
//     init (this.waterQuality.clarity = Medium)
//     init (this.plants.growthState = Moderate)
// }

pred init[l: Lake] {
    l.waterQuality.clarity = Medium
    l.plants.growthState = Moderate
    l.musselPopulation = MediumPopulation
}

// Temporal dynamics describing how Zebra Mussel populations influence water quality and plant growth
pred traces {
    init[Lake]
    always {
        // Update mussel population based on the number of mussels
        (#Lake.mussels <= 7) implies next_state Lake.musselPopulation = LowPopulation
        (#Lake.mussels > 7 and #Lake.mussels <= 14) implies next_state Lake.musselPopulation = MediumPopulation
        (#Lake.mussels > 14) implies next_state Lake.musselPopulation = HighPopulation

        // Mussel population affects water clarity
        (Lake.musselPopulation = LowPopulation) implies next_state Lake.waterQuality.clarity = Low
        (Lake.musselPopulation = MediumPopulation) implies next_state Lake.waterQuality.clarity = Medium
        (Lake.musselPopulation = HighPopulation) implies next_state Lake.waterQuality.clarity = High

        // Plant growth response to changes in water quality
        Lake.waterQuality.clarity = High implies next_state Lake.plants.growthState = Dense
        Lake.waterQuality.clarity = Low implies next_state Lake.plants.growthState = Sparse
        Lake.waterQuality.clarity = Medium implies next_state Lake.plants.growthState = Moderate
    }
}

// Run scenarios to check model behavior under different mussel population levels
run {
    eventually {
        // Lake.musselPopulation = LowPopulation
        // Lake.musselPopulation = MediumPopulation
        Lake.musselPopulation = HighPopulation
    }
} for 7 ZebraMussel, 1 Lake


//need to model the movement of states