use std::ffi::CStr;
use std::os::raw::c_char;

#[no_mangle]
fn alignment(first: *const c_char, second: *const c_char) -> u32 {
    let first_sequence = unsafe {
        assert!(!first.is_null());
        CStr::from_ptr(first)
    };
    let second_sequence = unsafe {
        assert!(!second.is_null());
        CStr::from_ptr(second)
    };
    let sequence1 = first_sequence.to_str().unwrap();
    let sequence2 = second_sequence.to_str().unwrap();
    return compute_matrix(sequence1, sequence2);
}

fn compute_matrix(sequence1: &str, sequence2: &str) -> u32 {
    let length_sequence1_width = sequence1.chars().count();
    let length_sequence2_height = sequence2.chars().count();
    
    let mut scoring_matrix = vec![vec![0; length_sequence1_width]; length_sequence2_height]; //nose mira aixo que soc MONGOLO
    for i in 0..length_sequence1_width {
        scoring_matrix[0][i] = i;
    }  
    for j in 0..length_sequence2_height {
        scoring_matrix[j][0] = j;
    }  
    for i in 1..length_sequence1_width {
        for j in 1..length_sequence2_height {
            let equal = if sequence1.chars().nth(i - 1) == sequence2.chars().nth(j - 1) {
                scoring_matrix[i - 1][j - 1]
            } else {
                scoring_matrix[i - 1][j - 1] + 1
            };
            let first_sequence_gap = scoring_matrix[i - 1][j];
            
            let second_sequence_gap = scoring_matrix[i][j - 1];
            scoring_matrix[i][j] = min(equal, first_sequence_gap, second_sequence_gap);
        }
    }
    let result = scoring_matrix[length_sequence1_width - 1][length_sequence2_height - 1] as u32;
    return result;
}
fn min(first_number: usize, second_number: usize, third_number: usize) -> usize {
    if first_number < second_number && first_number < third_number {
        return first_number;
    } else if second_number < third_number {
        return second_number;
    } else {
        return third_number;
    }
}
