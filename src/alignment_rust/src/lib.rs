use std::ffi::CStr;
use std::os::raw::c_char;
use std::cmp;

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
    let length_sequence1 = sequence1.chars().count();
    let length_sequence2 = sequence2.chars().count();
    let width = length_sequence1 + 1;
    let height = length_sequence2 + 1;

    let byte_sequence1 = sequence1.as_bytes();
    let byte_sequence2 = sequence2.as_bytes();

    let mut scoring_matrix = vec![vec![0; height]; width];

    for i in 0..width {
        scoring_matrix[i][0] = i;
    }
    for j in 0..height {
        scoring_matrix[0][j] = j;
    }

    for i in 1..width {
        let a = byte_sequence1[i - 1];
        for j in 1..height {
            let different = if i >= length_sequence1 || j >= length_sequence2 {
                true
            } else {
                false
            };
            let equal = if a == byte_sequence2[j - 1] && !different {
                scoring_matrix[i - 1][j - 1]
            } else {
                scoring_matrix[i - 1][j - 1] + 1
            };
            let first_sequence_gap = scoring_matrix[i - 1][j] + 1;
            let second_sequence_gap = scoring_matrix[i][j - 1] + 1;
            scoring_matrix[i][j] = cmp::min(cmp::min(equal, first_sequence_gap), second_sequence_gap);
        }
    }
    let result = scoring_matrix[width - 1][height - 1] - 1;
    return result as u32;
}
